# Generated by Django 5.0 on 2024-01-17 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_usercard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercard',
            name='expire_date',
            field=models.CharField(max_length=50),
        ),
    ]
