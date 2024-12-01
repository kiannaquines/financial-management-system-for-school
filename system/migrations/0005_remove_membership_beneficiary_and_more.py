# Generated by Django 5.1.1 on 2024-12-01 02:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_alter_membership_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='beneficiary',
        ),
        migrations.AlterField(
            model_name='membership',
            name='position',
            field=models.CharField(choices=[('ISAL', 'ISAL'), ('ALIVE', 'ALIVE'), ('Teacher 1', 'Teacher 1'), ('Teacher 2', 'Teacher 2'), ('Teacher 3', 'Teacher 3'), ('MS Teacher 1', 'MS Teacher 1'), ('MS Teacher 2', 'MS Teacher 2'), ('MS Teacher 3', 'MS Teacher 3'), ('School Head', 'School Head')], help_text='Position of the employee', max_length=50),
        ),
        migrations.AddField(
            model_name='membership',
            name='beneficiary',
            field=models.OneToOneField(blank=True, help_text='Select beneficiary of the employee, selecy only one.', null=True, on_delete=django.db.models.deletion.CASCADE, to='system.beneficiary'),
        ),
    ]