# Generated by Django 3.2.8 on 2021-12-11 04:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='textchoice',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]