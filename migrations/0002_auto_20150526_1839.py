# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='type',
        ),
        migrations.RemoveField(
            model_name='notificationsubscription',
            name='type',
        ),
        migrations.DeleteModel(
            name='NotificationType',
        ),
    ]
