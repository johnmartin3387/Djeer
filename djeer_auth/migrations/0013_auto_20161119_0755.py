# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0012_auto_20161118_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='booking',
            field=models.ForeignKey(blank=True, to='djeer_auth.Booking', null=True),
        ),
    ]
