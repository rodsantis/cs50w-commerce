# Generated by Django 5.0.4 on 2024-05-22 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_profile_listing_username_bid_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='username',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='username',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='username',
        ),
    ]
