# Generated by Django 4.0.6 on 2022-07-28 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogpage_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='likes',
        ),
    ]
