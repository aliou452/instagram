# Generated by Django 4.0.6 on 2022-07-29 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0012_alter_bloglikers_people'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='people',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenters_blog_relationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='creator',
            field=models.ForeignKey(help_text='The photo creator.', on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
