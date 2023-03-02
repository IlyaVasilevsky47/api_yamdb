# Generated by Django 3.2 on 2023-02-28 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230228_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewuser',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', help_text='Выберите из списка роль для пользователя', max_length=50, verbose_name='Роль пользователя'),
        ),
    ]
