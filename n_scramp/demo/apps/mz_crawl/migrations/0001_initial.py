# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='\u56de\u7b54\u5185\u5bb9')),
                ('is_accepted', models.BooleanField(default=False, db_index=True, verbose_name='\u88ab\u91c7\u7eb3')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898', db_index=True)),
                ('content', models.TextField(verbose_name='\u95ee\u9898\u5185\u5bb9')),
                ('src_url', models.URLField(verbose_name='\u6293\u53d6\u6e90\u8def\u5f84', db_index=True)),
                ('count_answer', models.IntegerField(verbose_name='\u56de\u7b54\u91cf', db_index=True)),
                ('count_view', models.IntegerField(verbose_name='\u6d4f\u89c8\u91cf', db_index=True)),
                ('weight', models.IntegerField(verbose_name='\u6743\u91cd', db_index=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u8bb0\u5f55\u65f6\u95f4')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=32, verbose_name='\u5173\u952e\u5b57(\u6587\u672c)', db_index=True)),
                ('question', models.ForeignKey(to='mz_crawl.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='mz_crawl.Question'),
            preserve_default=True,
        ),
    ]
