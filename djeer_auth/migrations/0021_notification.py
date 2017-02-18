# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0020_person_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.IntegerField(default=None, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(blank=True, to='djeer_auth.Person', null=True)),
            ],
            options={
                'db_table': 'Notification',
            },
        ),
    ]
