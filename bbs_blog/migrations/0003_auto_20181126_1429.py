# Generated by Django 2.0.9 on 2018-11-26 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbs_blog', '0002_auto_20181126_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bbs_blog.BlogIndex', verbose_name='个人博客'),
        ),
    ]
