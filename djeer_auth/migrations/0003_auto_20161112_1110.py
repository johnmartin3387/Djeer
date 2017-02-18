# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0002_auto_20161108_0223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='date',
            new_name='end_date',
        ),
        migrations.AddField(
            model_name='schedule',
            name='start_date',
            field=models.DateTimeField(default=None),
        ),
    ]
