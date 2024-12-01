# Generated by Django 5.1.1 on 2024-12-01 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_expenses_alter_assistance_assistance_evidence_second_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='expense_type',
            field=models.CharField(choices=[('Claims', 'Claims'), ('District Activities', 'District Activities'), ('Visitors Fund', 'Visitors Fund')], default='Claims', max_length=255),
            preserve_default=False,
        ),
    ]
