from django.db import models
from django.utils import timezone
from constructors.models import Constructor


class Driver(models.Model):
  driverId = models.IntegerField('Driver ID', null=True)
  number = models.CharField('Driver number', max_length=5, null=True)
  nationality = models.CharField('Nationality', max_length=80, null=True)
  driver_is_active = models.IntegerField('Is active')
  age = models.IntegerField('Age', null=True)
  full_name = models.CharField('Driver Name', max_length=250, null=True)
  driver_avg_point = models.DecimalField('Points AVG', null=True, max_digits=10, decimal_places=2)
  driver_avg_speed = models.DecimalField('Speed AVG', null=True, max_digits=10, decimal_places=2)
  race_end_bf_2015 = models.IntegerField('Race ends before 2015', null=True)
  race_end_in_2015 = models.IntegerField('Race ends in 2015', null=True)
  race_end_in_2016 = models.IntegerField('Race ends in 2016', null=True)
  race_end_in_2017 = models.IntegerField('Race ends in 2017', null=True)
  race_end_in_2018 = models.IntegerField('Race ends in 2018', null=True)
  race_end_in_2019 = models.IntegerField('Race ends in 2019', null=True)
  race_end_in_2020 = models.IntegerField('Race ends in 2020', null=True)
  race_end_in_2021 = models.IntegerField('Race ends in 2021', null=True)
  race_end_in_2022 = models.IntegerField('Race ends in 2022', null=True)
  race_end_in_2023 = models.IntegerField('Race ends in 2023', null=True)
  driver_most_won_circuit_id = models.IntegerField('Most won circuit ID', null=True)
  driver_nber_of_races_won = models.IntegerField('Number of races won', null=True)
  driver_nber_of_times_in_top_10 = models.IntegerField('Number of time in the top 10', null=True)
  constructorId = models.ForeignKey(Constructor, on_delete=models.CASCADE)
  createdDate = models.DateTimeField(blank=True, editable=False, default=timezone.now)
  updateDate = models.DateTimeField(blank=True, editable=False, null=True)
  isArchived = models.BooleanField(default=False, blank=True)
  # TODO Add the picture of the driver

  def save(self, *args, **kwargs):
    """ 
      Override On save method because we want to update the update date when we save this 
      kind of object
    """
    if self.id:
      # Write the update date automatically when we update the object
      self.updateDate = timezone.now()
      return super(Driver, self).save(*args, **kwargs)


