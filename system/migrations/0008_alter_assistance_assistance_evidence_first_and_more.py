# Generated by Django 5.1.1 on 2024-09-30 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_assistance_date_released'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistance',
            name='assistance_evidence_first',
            field=models.ImageField(upload_to='assistance/proof/'),
        ),
        migrations.AlterField(
            model_name='assistance',
            name='assistance_evidence_second',
            field=models.ImageField(upload_to='assistance/proof/'),
        ),
    ]
