# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginsys', '0003_auto_20150721_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_active',
        ),
    ]
