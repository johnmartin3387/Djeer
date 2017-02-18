# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0025_help_sort'),
    ]

    operations = [
        migrations.AlterField(
            model_name='help',
            name='content',
            field=tinymce.models.HTMLField(default='', null=True, blank=True),
        ),
    ]
