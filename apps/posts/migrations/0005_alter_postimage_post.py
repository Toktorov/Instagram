# Generated by Django 3.2.3 on 2021-05-28 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_postimage_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_image', to='posts.post'),
        ),
    ]
