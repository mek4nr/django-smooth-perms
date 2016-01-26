# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmoothGroup',
            fields=[
                ('group_ptr', models.OneToOneField(to='auth.Group', serialize=False, primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'User groups (SmoothPerm)',
                'verbose_name': 'User group (SmoothPerm)',
            },
            bases=('auth.group',),
        ),
        migrations.CreateModel(
            name='SmoothUser',
            fields=[
                ('user_ptr', models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'verbose_name_plural': 'Users (SmoothPerm)',
                'verbose_name': 'User (SmoothPerm)',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
