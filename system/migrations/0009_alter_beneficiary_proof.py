# Generated by Django 5.1.1 on 2024-09-30 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_alter_assistance_assistance_evidence_first_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='proof',
            field=models.ImageField(upload_to='beneficiary/proof/'),
        ),
    ]
