from django.core.management.base import BaseCommand
from gws.models import Slope, SkiLift, Restaurant, StoppingPlace

class Command(BaseCommand):
	def handle(self, *args, **options):
		Slope.objects.all().delete()
		SkiLift.objects.all().delete()
		Restaurant.objects.all().delete()
		StoppingPlace.objects.all().delete()
