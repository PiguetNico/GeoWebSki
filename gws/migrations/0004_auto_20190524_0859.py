# Generated by Django 2.2.1 on 2019-05-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gws', '0003_auto_20190524_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='skilift',
            name='open',
            field=models.BooleanField(default=False, verbose_name='Ski Lift open?'),
        ),
        migrations.AddField(
            model_name='skilift',
            name='twoways',
            field=models.BooleanField(default=False, verbose_name='Two way lift?'),
        ),
    ]