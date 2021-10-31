# Generated by Django 3.2.8 on 2021-10-25 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211025_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='place',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.teachers'),
        ),
    ]
