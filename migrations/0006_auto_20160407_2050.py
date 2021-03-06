# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20150601_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='importance',
            field=models.CharField(choices=[(b'low', b'Low'), (b'medium', b'Medium'), (b'high', b'High')], max_length=10),
        ),
        migrations.AlterField(
            model_name='notificationsubscription',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_subscriptions', to='notifications.NotificationType'),
        ),
    ]
