# Generated by Django 5.1.1 on 2024-12-04 23:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_alter_schoolyear_primary_school_year_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='schoolyear',
            name='unique_primary_school_year',
        ),
        migrations.AddField(
            model_name='assistance',
            name='school_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assistance_school_year', to='system.schoolyear'),
        ),
        migrations.AddField(
            model_name='expenses',
            name='school_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expense_school_year', to='system.schoolyear'),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='school_year_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_year_transaction', to='system.schoolyear'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='school_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.schoolyear'),
        ),
        migrations.AddConstraint(
            model_name='schoolyear',
            constraint=models.UniqueConstraint(condition=models.Q(('primary_school_year', True)), fields=('primary_school_year',), name='unique_primary_school_year', violation_error_message='Only one primary school year should be specified, please try again later.'),
        ),
    ]
