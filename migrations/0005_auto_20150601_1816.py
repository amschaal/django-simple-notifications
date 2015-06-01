# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20150526_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationsubscription',
            name='subscribe',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='notificationsubscription',
            unique_together=set([('user', 'type')]),
        ),
    ]
