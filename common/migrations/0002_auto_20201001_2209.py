# Generated by Django 3.1.1 on 2020-10-01 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanner',
            name='Charge',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='scanner',
            name='LastRegister',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
