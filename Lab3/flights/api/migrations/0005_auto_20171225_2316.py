# Generated by Django 2.0 on 2017-12-25 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20171225_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airplane',
            name='builddate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='pilot',
            name='starting_date',
            field=models.DateField(),
        ),
    ]
