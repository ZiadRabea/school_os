# Generated by Django 5.0.7 on 2024-09-04 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_profile_school'),
        ('teachers', '0002_alter_teacher_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='constant',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Accounts.profile'),
            preserve_default=False,
        ),
    ]
