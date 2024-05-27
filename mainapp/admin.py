from django.contrib import admin
from mainapp import models
from django.utils.html import format_html

# Register your models here.
#admin.site.register(models.Event)
admin.site.register(models.Ticket)
admin.site.register(models.Reservation)
admin.site.register(models.UserCard)
admin.site.register(models.Venue)

class EventModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'formatted_description')

    def formatted_description(self, obj):
        # Replace newlines with <br> tags for line breaks
        return format_html(obj.description.replace('\n', '<br>'))

    formatted_description.short_description = 'Description'

admin.site.register(models.Event, EventModelAdmin)

