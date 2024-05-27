from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint


from django.shortcuts import render, redirect, get_object_or_404
from mainapp import models, forms
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from dotenv import load_dotenv
import os

from datetime import date

# Create your views here.

def homepage(request):
    return render(request, 'mainapp/home.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('login_page')
    return render(request, 'mainapp/login.html')


def logout_page(request):
    logout(request)
    messages.success(request, ("Logged out succesfully"))
    return redirect('home')



def register_page(request):
    if request.method != 'POST':
        form = forms.CustomUserForm()
    else:
        form = forms.CustomUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            configuration = sib_api_v3_sdk.Configuration()
            load_dotenv()
            API_KEY = os.getenv('API_KEY')
            configuration.api_key['api-key'] = API_KEY

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = "Welcome to QuickTicket"
            template_path = 'mainapp/email_messages/new_signup.html'
            user_context = {'user': new_user}
            html_content = render_to_string(template_path, user_context)
            sender = {"name":"QuickTicket","email":"byteexplorer7@gmail.com"}
            to = [{"email":new_user.email,"name": "NewUser"}]
            headers = {"Some-Custom-Name":"unique-id-1234"}
            params = {"parameter":"My param value","subject":"New Subject"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                pprint(api_response)
            except ApiException as e:
                print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            return redirect('home')

    context = {'form': form}

    return render(request, 'mainapp/register.html', context)


class AddVenue(UserPassesTestMixin, CreateView):
    form_class = forms.VenueForm
    template_name = 'mainapp/add_venue.html'
    success_url = 'venues'
    model = models.Venue

    def test_func(self):
        return self.request.user.username.startswith('altyn')
    

    def handle_no_permission(self):
        return render(
            self.request,
            'mainapp/forbidden.html',
            {'redirect_url': 'forbidden'}
        )

    def get_login_url(self) -> str:
        return ('forbidden')


def events(request, category):
    # Assuming 'category' is passed as an argument in the URL
    event_category = category.lower()  # Convert to lowercase for case-insensitivity

    # Fetch events based on the category
    if event_category in ['theater', 'sport', 'concert', 'culture']:
        category_events = models.Event.objects.filter(type=event_category)
        context = {'events': category_events, 'event_category': event_category}
        return render(request, 'mainapp/events/category_events.html', context)
    else:
        return render(request, 'mainapp/home.html')



class Events(ListView):
    model = models.Event
    template_name = 'mainapp/home.html'
    context_object_name = 'all_events'


class EventDetails(DetailView):
    model = models.Event
    template_name = 'mainapp/events/event_detail.html'
    context_object_name = 'event'
    pk_url_kwarg ='id'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context


@login_required(login_url="login", redirect_field_name="make_reservation")
def tickets(request, id):
    event = models.Event.objects.get(id=id)
    ticket = models.Ticket.objects.filter(event=event)
    ticket_price = ticket[0].price

    if request.method == 'POST':
        nr_bilete = int(request.POST.get('nr_bilete', 0))

        # Check if there are available tickets
        if nr_bilete <= event.total_tickets:
            print('nr_tickets: ', nr_bilete)
            # If there are available tickets, you can redirect to the card information page
            # Replace 'card_info_page' with the actual URL or view name for the card information page
            return redirect('user_card_info', id=event.id, nr_bilete=nr_bilete)
        else:
            # Handle the case where there are not enough available tickets
            # You may want to render a page indicating the unavailability of tickets or handle it accordingly
            #return render(request, 'unavailable_tickets.html')
            return render(request, 'example.html')

    context =  {'event': event, 'ticket_price': ticket_price}
    # Render the reserve ticket page with the event details for the GET request
    return render(request, 'mainapp/events/tickets.html', context)


def user_card_info(request, id, nr_bilete):
    event = models.Event.objects.get(id=id)
    ticket = models.Ticket.objects.filter(event=event)
    ticket_price = ticket[0].price
    ticket_price = float(ticket_price.split(' ')[0])
    total_price = int(nr_bilete) * ticket_price
    context = {'event': event, 'total_price': total_price, 'nr_bilete': nr_bilete}
    if request.method == 'POST':
        card_number = request.POST.get('cardNumber')
        card_type = request.POST.get('cardType')
        expiry_date = request.POST.get('expiryDate')
        cvv = request.POST.get('cvv')

        # Create a UserCard object and save it to the database
        user_card = models.UserCard(
            card_number=card_number,
            card_type=card_type,
            expiry_date=expiry_date,
            cvv=cvv
        )
        user_card.save()

        return redirect('make_reservation', id=event.id, nr_bilete=nr_bilete)
    
    return render(request, 'mainapp/user_card_info.html', context)



def make_reservation(request, id, nr_bilete):
    event = models.Event.objects.get(id=id)
    if request.method == 'POST':
        try:
            reservation = models.Reservation(
                    reservation_date=date.today(),
                    ticket_quantity=nr_bilete,
                    user=request.user,  # Assuming you have user authentication
                    event=event,
                )
            reservation.save()

            if event.total_tickets > nr_bilete:
                event.total_tickets -= nr_bilete
                event.save()
            else:
                return render(request, 'example.html')

            # send email for successful registration
            configuration = sib_api_v3_sdk.Configuration()
            load_dotenv()
            API_KEY = os.getenv('API_KEY')
            configuration.api_key['api-key'] = API_KEY

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = "Reservation Success"
            template_path = 'mainapp/reservations/reservation_email.html'
            user_context = {'user': request.user, 'reservation': reservation}
            html_content = render_to_string(template_path, user_context)
            sender = {"name":"QuickTicket","email":"byteexplorer7@gmail.com"}
            to = [{"email": request.user.email,"name": "Success"}]
            headers = {"Some-Custom-Name":"unique-id-1234"}
            #params = {"parameter":"My param value","subject":"New Subject"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                pprint(api_response)
            except ApiException as e:
                print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

            
            # Redirect or return an appropriate response
            return redirect('reservation_detail', id=reservation.id)  # Replace 'success_page' with your success page URL
        except ValueError:
            messages.error(request, 'Invalid ticket ID')

    # Redirect or return an appropriate response
    return redirect('event_detail')  # Replace 'error_page' with your error page URL


class ReservationDetail(DetailView):
    model = models.Reservation
    template_name = 'mainapp/reservations/reservation_detail.html'
    context_object_name = 'reservation'
    pk_url_kwarg ='id'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        return context  
    

def delete_reservation(request, pk):
    reservation = models.Reservation.objects.get(id=pk)

    if request.method == 'POST':
        # Perform deletion logic
        reservation.delete()
        return redirect('home')  # Redirect to a success page or another view

    return render(request, 'mainapp/reservations/delete_reservation_confirm.html', {'reservation': reservation})

