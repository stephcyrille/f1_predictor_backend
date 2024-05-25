import csv
from drivers.models import Driver
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
  help = 'Import data from CSV file to Driver model'

  def add_arguments(self, parser):
    parser.add_argument('csv_file', type=str, help='The path to the CSV file')

  def handle(self, *args, **kwargs):
    csv_file = kwargs['csv_file']
    with open(csv_file, 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        try:
          driver = Driver(
            driverId=row['driverId'],
            number=row['number'],
            nationality=row['nationality'],
            driver_is_active=row['driver_is_active'],
            age=row['age'],
            full_name=row['full_name'],
            driver_avg_point=row['driver_avg_point'],
            driver_avg_speed=row['driver_avg_speed'],
            race_end_bf_2015=row['race_end_bf_2015'],
            race_end_in_2015=row['race_end_in_2015'],
            race_end_in_2016=row['race_end_in_2016'],
            race_end_in_2017=row['race_end_in_2017'],
            race_end_in_2018=row['race_end_in_2018'],
            race_end_in_2019=row['race_end_in_2019'],
            race_end_in_2020=row['race_end_in_2020'],
            race_end_in_2021=row['race_end_in_2021'],
            race_end_in_2022=row['race_end_in_2022'],
            race_end_in_2023=row['race_end_in_2023'],
            driver_most_won_circuit_id=row['driver_most_won_circuit_id'],
            driver_nber_of_races_won=row['driver_nber_of_races_won'],
            driver_nber_of_times_in_top_10=row['driver_nber_of_times_in_top_10'],
            createdDate=timezone.now()
          )
          driver.save()
        except Exception as e:
          self.stdout.write(self.style.ERROR(f'Error importing Drivers Data: {e}'))
    self.stdout.write(self.style.SUCCESS('Drivers Data imported successfully'))
