# Generated by Django 3.1.5 on 2021-03-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20201019_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanner',
            name='CommandMode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='scanner',
            name='State',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
