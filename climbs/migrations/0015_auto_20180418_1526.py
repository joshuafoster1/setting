# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-18 22:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climbs', '0014_auto_20180417_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField()),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='global_spread', to='climbs.Grade')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='global_spread', to='climbs.Gym')),
            ],
        ),
        migrations.RenameModel(
            old_name='AreaSpread',
            new_name='LocalDistribution',
        ),
        migrations.RemoveField(
            model_name='spread',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='spread',
            name='gym',
        ),
        migrations.DeleteModel(
            name='Spread',
        ),
    ]
