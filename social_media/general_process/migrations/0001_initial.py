# Generated by Django 5.0.1 on 2024-01-15 08:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('explore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFavorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category_count', models.IntegerField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('like_count', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('comments_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
                ('posts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explore.posts')),
            ],
        ),
        migrations.CreateModel(
            name='Comment_like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('comment_like_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general_process.comments')),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_favorite_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general_process.categoryfavorites')),
                ('posts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explore.posts')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.customuser')),
                ('posts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='explore.posts')),
            ],
        ),
    ]
