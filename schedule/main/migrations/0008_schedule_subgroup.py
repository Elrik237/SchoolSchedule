# Generated by Django 3.2.8 on 2021-10-31 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20211031_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='subgroup',
            field=models.IntegerField(default=None, verbose_name='Подгруппа'),
        ),
    ]