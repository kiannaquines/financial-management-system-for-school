# Generated by Django 5.1.1 on 2024-09-28 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_assistance_request_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assistance',
            old_name='assistance_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='beneficiary',
            old_name='beneficiary_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='membership',
            old_name='membership_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='payment_id',
            new_name='id',
        ),
    ]