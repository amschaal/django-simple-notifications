# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150526_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.ForeignKey(blank=True, to='notifications.NotificationType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificationsubscription',
            name='type',
            field=models.ForeignKey(default=None, to='notifications.NotificationType'),
            preserve_default=False,
        ),
    ]
