# Generated by Django 3.1.7 on 2021-04-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210406_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatat',
            field=models.ImageField(blank=True, null=True, upload_to='users/avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('м', 'мужской'), ('ж', 'женский')], default=' ', max_length=1, verbose_name='Пол'),
        ),
    ]
