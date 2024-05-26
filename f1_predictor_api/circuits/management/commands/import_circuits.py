import csv
from circuits.models import Circuit
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
  help = 'Import data from CSV file to Circuit model'

  def add_arguments(self, parser):
    parser.add_argument('csv_file', type=str, help='The path to the CSV file')

  def handle(self, *args, **kwargs):
    if Circuit.objects.exists():
      self.stdout.write(self.style.WARNING('Circuit Data already imported'))
      return
    csv_file = kwargs['csv_file']
    with open(csv_file, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        try:
          circuit = Circuit(
            circuitId=row['circuitId'],
            name=row['name'],
            location=row['location'],
            country=row['country'],
            lat=row['lat'],
            lng=row['lng'],
            circuits_is_active=row['circuits_is_active'],
            createdDate=timezone.now()
          )
          circuit.save()
        except Exception as e:
          self.stdout.write(self.style.ERROR(f'Error importing Circuit Data: {e}'))
    self.stdout.write(self.style.SUCCESS('Circuit Data imported successfully'))
