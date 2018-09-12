# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mz_crawl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count_answer', models.IntegerField(verbose_name='\u56de\u7b54\u91cf', db_index=True)),
                ('count_view', models.IntegerField(verbose_name='\u6d4f\u89c8\u91cf', db_index=True)),
                ('crawl_time', models.DateTimeField(verbose_name='\u6293\u53d6\u65f6\u95f4')),
                ('question', models.ForeignKey(to='mz_crawl.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='crawl_time',
            field=models.DateTimeField(null=True, verbose_name='\u6700\u540e\u722c\u53d6\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='speed_view',
            field=models.FloatField(null=True, verbose_name='\u6bcf\u5c0f\u65f6\u6d4f\u89c8\u589e\u957f\u91cf', db_index=True),
            preserve_default=True,
        ),
    ]
