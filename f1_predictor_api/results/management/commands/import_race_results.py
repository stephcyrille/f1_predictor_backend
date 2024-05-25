import csv
from results.models import RaceResult
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = 'Import data from CSV file to RaceResult model'

  def add_arguments(self, parser):
    parser.add_argument('csv_file', type=str, help='The path to the CSV file')

  def handle(self, *args, **kwargs):
    csv_file = kwargs['csv_file']
    with open(csv_file, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        race_results = RaceResult(
          resultId=row['resultId'],
          raceId=row['raceId'],
          driverId=row['driverId'],
          constructorId=row['constructorId'],
          circuitId=row['circuitId'],
          statusId=row['statusId'],
          grid=row['grid'],
          race_rank=row['race_rank'],
          points=row['points'],
          laps=row['laps'],
          milliseconds=row['milliseconds'],
          fastestLap=row['fastestLap'],
          fastestLapTime=row['fastestLapTime'],
          fastestLapSpeed=row['fastestLapSpeed'],
          year=row['year'],
          round=row['round'],
          name=row['name']
        )
        race_results.save()
    self.stdout.write(self.style.SUCCESS('Race results Data imported successfully'))
