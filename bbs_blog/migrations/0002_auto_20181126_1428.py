# Generated by Django 2.0.9 on 2018-11-26 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bbs_blog.BlogIndex', verbose_name='个人博客'),
        ),
    ]
