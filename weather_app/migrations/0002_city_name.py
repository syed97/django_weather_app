# Generated by Django 4.0.3 on 2022-03-28 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='name',
            field=models.CharField(default='Karachi', max_length=30),
        ),
    ]
