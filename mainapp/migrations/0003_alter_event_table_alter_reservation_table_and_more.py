# Generated by Django 5.0 on 2023-12-26 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_event_event_logo_venue_map_location'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='event',
            table='event',
        ),
        migrations.AlterModelTable(
            name='reservation',
            table='reservation',
        ),
        migrations.AlterModelTable(
            name='ticket',
            table='ticket',
        ),
        migrations.AlterModelTable(
            name='usercard',
            table='user_card',
        ),
        migrations.AlterModelTable(
            name='venue',
            table='venue',
        ),
    ]
