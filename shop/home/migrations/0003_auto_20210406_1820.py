# Generated by Django 3.1.7 on 2021-04-06 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210329_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(help_text='Выберите бренд товара', on_delete=django.db.models.deletion.CASCADE, to='home.brand', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию товара', on_delete=django.db.models.deletion.CASCADE, to='home.category', verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='product',
            name='made_in',
            field=models.ForeignKey(help_text='Выберите страну производителя', on_delete=django.db.models.deletion.CASCADE, to='home.madein', verbose_name='Сделано в'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(blank=True, help_text='Выберите подкатегорию товара', null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subcategory', verbose_name='Название подкатегории'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.CASCADE, to='home.category', verbose_name='Категория'),
        ),
    ]
