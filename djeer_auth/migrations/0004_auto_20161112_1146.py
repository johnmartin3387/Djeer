# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0003_auto_20161112_1110'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scheduled',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='scheduled',
            name='dj',
        ),
        migrations.RemoveField(
            model_name='scheduled',
            name='schedule',
        ),
        migrations.AddField(
            model_name='schedule',
            name='dj',
            field=models.ForeignKey(blank=True, to='djeer_auth.Dj', null=True),
        ),
        migrations.DeleteModel(
            name='Scheduled',
        ),
    ]
