# Generated by Django 4.0.6 on 2022-07-29 02:56

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('blog', '0010_blogindexpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumPage',
            fields=[
                ('blogpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.blogpage')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogpage',),
        ),
        migrations.CreateModel(
            name='AlbumPhotos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('album_image', models.ForeignKey(blank=True, help_text='Landscape mode only; horizontal width between 1000px and 3000px.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='album_photo', to='blog.albumpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
