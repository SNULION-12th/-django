# Generated by Django 5.0.4 on 2024-05-14 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like_users',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]