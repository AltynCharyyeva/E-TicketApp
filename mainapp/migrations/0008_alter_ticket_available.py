# Generated by Django 5.0 on 2023-12-29 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_ticket_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='available',
            field=models.CharField(max_length=20, null=True),
        ),
    ]