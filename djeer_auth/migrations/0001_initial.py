# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hourly_rate', models.IntegerField(null=True, blank=True)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'Bid',
            },
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Billing',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.TextField()),
                ('message', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, null=True, blank=True)),
                ('bid', models.ForeignKey(blank=True, to='djeer_auth.Bid', null=True)),
            ],
            options={
                'db_table': 'booking',
            },
        ),
        migrations.CreateModel(
            name='Dj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('rate', models.IntegerField(null=True, blank=True)),
                ('discount_rate', models.IntegerField(null=True, blank=True)),
                ('discount_hour', models.IntegerField(null=True, blank=True)),
                ('booked_num', models.IntegerField(null=True, blank=True)),
                ('transactions', models.IntegerField(null=True, blank=True)),
                ('responses', models.IntegerField(null=True, blank=True)),
                ('avg_response_time', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'DJ',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Equipment',
            },
        ),
        migrations.CreateModel(
            name='Equipped',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dj', models.ForeignKey(blank=True, to='djeer_auth.Dj', null=True)),
                ('equipment', models.ForeignKey(blank=True, to='djeer_auth.Equipment', null=True)),
            ],
            options={
                'db_table': 'Equipped',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('date', models.DateField()),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('type', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=100)),
                ('address', models.ForeignKey(blank=True, to='djeer_auth.Address', null=True)),
            ],
            options={
                'db_table': 'Event',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Host',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10)),
                ('card_number', models.CharField(max_length=100)),
                ('expires_on', models.DateTimeField(null=True, blank=True)),
                ('security_code', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True, blank=True)),
                ('gender', models.IntegerField(null=True, blank=True)),
                ('birthday', models.DateTimeField()),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.CharField(max_length=255, null=True, blank=True)),
                ('profile_url', models.URLField(null=True, blank=True)),
                ('role', models.CharField(max_length=10, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('address', models.ForeignKey(blank=True, to='djeer_auth.Address', null=True)),
                ('bill', models.ForeignKey(blank=True, to='djeer_auth.Billing', null=True)),
            ],
            options={
                'db_table': 'Person',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo_url', models.CharField(max_length=255)),
                ('dj', models.ForeignKey(blank=True, to='djeer_auth.Dj', null=True)),
            ],
            options={
                'db_table': 'Photo',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feedback', models.TextField(null=True, blank=True)),
                ('score', models.IntegerField(null=True, blank=True)),
                ('communication', models.IntegerField(null=True, blank=True)),
                ('professionalism', models.IntegerField(null=True, blank=True)),
                ('accuracy', models.IntegerField(null=True, blank=True)),
                ('track', models.IntegerField(null=True, blank=True)),
                ('mixing', models.IntegerField(null=True, blank=True)),
                ('success', models.CharField(max_length=50, null=True, blank=True)),
                ('amount', models.IntegerField(null=True, blank=True)),
                ('paid_out', models.IntegerField(null=True, blank=True)),
                ('transaction_id', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('availability', models.BooleanField(default=False)),
                ('rate', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'Schedule',
            },
        ),
        migrations.CreateModel(
            name='Scheduled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dj', models.ForeignKey(blank=True, to='djeer_auth.Dj', null=True)),
                ('schedule', models.ForeignKey(blank=True, to='djeer_auth.Schedule', null=True)),
            ],
            options={
                'db_table': 'Scheduled',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_notification', models.CharField(max_length=255, null=True, blank=True)),
                ('mobile_notification', models.CharField(max_length=255, null=True, blank=True)),
                ('facebook', models.CharField(max_length=255, null=True, blank=True)),
                ('search_engine', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'Setting',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='setting',
            field=models.ForeignKey(blank=True, to='djeer_auth.Setting', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='person',
            field=models.ForeignKey(blank=True, to='djeer_auth.Person', null=True),
        ),
        migrations.AddField(
            model_name='host',
            name='person',
            field=models.ForeignKey(blank=True, to='djeer_auth.Person', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(blank=True, to='djeer_auth.Host', null=True),
        ),
        migrations.AddField(
            model_name='dj',
            name='person',
            field=models.ForeignKey(blank=True, to='djeer_auth.Person', null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='event',
            field=models.ForeignKey(blank=True, to='djeer_auth.Event', null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='review',
            field=models.ForeignKey(blank=True, to='djeer_auth.Review', null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='dj',
            field=models.ForeignKey(blank=True, to='djeer_auth.Dj', null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='event',
            field=models.ForeignKey(blank=True, to='djeer_auth.Event', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='scheduled',
            unique_together=set([('schedule', 'dj')]),
        ),
        migrations.AlterUniqueTogether(
            name='equipped',
            unique_together=set([('equipment', 'dj')]),
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together=set([('bid', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='bid',
            unique_together=set([('id', 'event')]),
        ),
    ]
