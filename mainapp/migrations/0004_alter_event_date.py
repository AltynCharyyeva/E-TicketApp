# Generated by Django 5.0 on 2023-12-26 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_event_table_alter_reservation_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.CharField(max_length=50),
        ),
    ]
