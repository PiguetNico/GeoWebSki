# Generated by Django 2.2.1 on 2019-05-26 12:36

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, verbose_name='Restaurant name')),
                ('capacity', models.IntegerField(null=True, verbose_name='Capacity (nb. of people)')),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name="Restaurant's location")),
            ],
        ),
        migrations.CreateModel(
            name='SkiLift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, verbose_name='Ski lift name')),
                ('hourly_flow', models.IntegerField(verbose_name='Hourly flow (in nb. of people)')),
                ('track', django.contrib.gis.db.models.fields.LineStringField(srid=4326, verbose_name='Ski lift geographic track')),
                ('open', models.BooleanField(default=False, verbose_name='Ski Lift open?')),
                ('twoways', models.BooleanField(default=False, verbose_name='Two way lift?')),
            ],
        ),
        migrations.CreateModel(
            name='Slope',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, verbose_name='Slope name')),
                ('color', models.CharField(choices=[('blue', 'Blue (easy)'), ('red', 'Red (medium)'), ('black', 'Black (hard)')], max_length=80, null=True, verbose_name='Slope difficulty')),
                ('open', models.BooleanField(default=False, verbose_name='Slope open?')),
                ('area', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name='Slope geographic area')),
            ],
        ),
        migrations.CreateModel(
            name='StoppingPlace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('altitude', models.IntegerField(null=True, verbose_name='Altitude (in meters)')),
                ('area', django.contrib.gis.db.models.fields.PolygonField(srid=4326, verbose_name="Stopping place's area")),
            ],
        ),
    ]
