# Generated by Django 4.2.13 on 2024-06-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audits', '0002_audit_assigned_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
