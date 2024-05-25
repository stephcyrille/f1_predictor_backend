import csv
from constructors.models import Constructor
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = 'Import data from CSV file to Constructor model'

  def add_arguments(self, parser):
    parser.add_argument('csv_file', type=str, help='The path to the CSV file')

  def handle(self, *args, **kwargs):
    csv_file = kwargs['csv_file']
    with open(csv_file, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        constructor = Constructor(
          constructorId=row['constructorId'],
          constructor_name=row['constructor_name'],
          constructor_country=row['constructor_country'],
          constructor_is_active=row['constructor_is_active'],
          constructor_races_won=row['constructor_races_won'],
          constructor_avg_point=row['constructor_avg_point'],
          constructor_times_in_top_10=row['constructor_times_in_top_10']
        )
        constructor.save()
    self.stdout.write(self.style.SUCCESS('Constructors Data imported successfully'))
