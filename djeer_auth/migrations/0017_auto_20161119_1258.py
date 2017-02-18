# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djeer_auth', '0016_auto_20161119_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='price',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dj',
            name='discount_rate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dj',
            name='rate',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dj',
            name='score',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='accuracy',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='amount',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='communication',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='mixing',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='paid_out',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='professionalism',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='track',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='rate',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
