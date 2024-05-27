from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Venue(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    map_location=models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        db_table = 'venue'    


class Event(models.Model):
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    description=models.TextField()
    total_tickets=models.IntegerField(null=True)
    venue=models.ForeignKey(Venue, on_delete=models.CASCADE, blank=True, null=True)
    event_logo=models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        db_table = 'event'


class Ticket(models.Model):
    price=models.CharField(max_length=50)
    type=models.CharField(max_length=10)
    seat_number=models.CharField(max_length=10)
    event=models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    available = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return f'{self.event}'
    
    class Meta:
        db_table = 'ticket'


class Reservation(models.Model):
    reservation_date=models.DateTimeField()
    ticket_quantity=models.CharField(max_length=10)
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    event=models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.event} {self.user}'
    
    class Meta:
        db_table = 'reservation'

class UserCard(models.Model):
    expiry_date=models.CharField(max_length=50)
    card_number=models.CharField(max_length=50)
    card_type=models.CharField(max_length=50)
    cvv=models.CharField(max_length=3)
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # def __str__(self) -> str:
    #     return f'{self.course_name}'
    
    class Meta:
        db_table = 'user_card'


