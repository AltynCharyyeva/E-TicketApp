from django.urls import path
from mainapp import views

urlpatterns = [
   path('', views.Events.as_view(), name='home'),
   path('login', views.login_page, name='login'),
   path('logout', views.logout_page, name='logout'),
   path('register', views.register_page, name='register'),
   #path('events/all_events', views.Events.as_view(), name='all_events'),
   path('events/<str:category>/', views.events, name='events'),
   path('events/event_detail/<int:id>', views.EventDetails.as_view(), name='event_detail'),
   path('events/event_detail/<int:id>/tickets', views.tickets, name='tickets'),
   path('events/event_detail/<int:id>/tickets/user_card_info/<int:nr_bilete>/', views.user_card_info, name='user_card_info'),
   path('make_reservation/<int:id>/<int:nr_bilete>', views.make_reservation, name='make_reservation'),
   path('reservations/reservation_detail/<int:id>', views.ReservationDetail.as_view(), name='reservation_detail'),
   path('reservation/<int:pk>/delete/', views.delete_reservation, name='delete_reservation'),
]