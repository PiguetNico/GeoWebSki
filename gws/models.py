from django.db import models


# Create your models here.
class Slope(models.Model):
    SLOPE_COLORS = (
        ('blue', 'Blue (easy)'),
        ('red', 'Red (medium)'),
        ('black', 'Black (hard)')
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField('Slope name', max_length=80)
    color = models.CharField('Slope difficulty', max_length=80, choices=SLOPE_COLORS, null=True)
    open = models.BooleanField('Slope open?', default=False)


class SkiLift(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Ski lift name', max_length=80)
    hourly_flow = models.IntegerField('Hourly flow (in nb. of people)', )


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Restaurant name', max_length=80)
    capacity = models.IntegerField('Capacity (nb. of people)', null=True)
