# Generated by Django 5.0.7 on 2024-09-04 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_profile_school'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.profile'),
        ),
    ]
