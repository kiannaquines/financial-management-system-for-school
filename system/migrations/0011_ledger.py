# Generated by Django 5.1.1 on 2024-12-02 11:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_unenrollreason_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField()),
                ('description', models.TextField(max_length=255)),
                ('amount', models.FloatField()),
                ('transaction_type', models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], max_length=255)),
                ('date_transaction', models.DateTimeField(auto_now_add=True)),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
