# Generated by Django 2.0 on 2017-12-25 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='airplane_id',
            new_name='airplane',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='arrival_airport_id',
            new_name='arrival_airport',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='departure_airport_id',
            new_name='departure_airport',
        ),
    ]