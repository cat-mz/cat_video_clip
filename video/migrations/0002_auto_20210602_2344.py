# Generated by Django 3.2.3 on 2021-06-02 15:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户管理类', 'verbose_name_plural': '用户管理类'},
        ),
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(default=django.utils.timezone.now, max_length=11, unique=True, verbose_name='手机号码'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='user',
            table='tb_users',
        ),
    ]
