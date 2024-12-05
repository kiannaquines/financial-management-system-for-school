# Generated by Django 5.1.1 on 2024-12-04 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolyear',
            name='primary_school_year',
            field=models.BooleanField(default=False, help_text='Toggle for primary school years', unique=True),
        ),
    ]
