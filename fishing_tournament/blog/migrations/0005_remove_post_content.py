# Generated by Django 2.1.5 on 2019-11-06 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
    ]