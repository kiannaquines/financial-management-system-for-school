# Generated by Django 5.1.1 on 2024-12-05 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_alter_dependents_options_alter_ledger_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assistance',
            name='amount_released',
            field=models.DecimalField(decimal_places=2, help_text='Amount applied in assistance', max_digits=10),
        ),
    ]
