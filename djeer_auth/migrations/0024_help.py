# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0023_notification_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('content', models.TextField(default='', null=True, blank=True)),
                ('parent', models.ForeignKey(blank=True, to='djeer_auth.Help', null=True)),
            ],
            options={
                'db_table': 'Help',
            },
        ),
    ]
