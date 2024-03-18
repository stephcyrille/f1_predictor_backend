from django.db import models
from django.utils import timezone


class RaceResult(models.Model):
  resultId = models.IntegerField('Result ID', unique=True, blank=True)  
  raceId = models.IntegerField('Race ID', blank=True)  
  driverId = models.IntegerField('Driver ID', blank=True)  
  constructorId = models.IntegerField('Constructor ID', blank=True)  
  circuitId = models.IntegerField('Circuit ID', blank=True)  
  statusId = models.IntegerField('Status ID', blank=True)  
  grid = models.IntegerField('Grid position', blank=True)  
  race_rank = models.IntegerField('Race rank', blank=True)  
  points = models.DecimalField('Driver point', max_digits=10, decimal_places=2, blank=True)
  laps = models.IntegerField('Lap number', blank=True)  
  milliseconds = models.IntegerField('Time (in ms)', blank=True)  
  fastestLap = models.IntegerField('Fastes lap', blank=True)  
  fastestLapTime = models.IntegerField('Fastest lap time (in ms)', blank=True)  
  fastestLapSpeed = models.DecimalField('Fastest lap speed', max_digits=10, decimal_places=2, blank=True)
  year = models.IntegerField('Year', blank=True)  
  round = models.IntegerField('Round', blank=True)  
  name = models.CharField('Circuit name', max_length=150, blank=True) 
  createdDate = models.DateTimeField(blank=True, editable=False, default=timezone.now)
  updateDate = models.DateTimeField(blank=True, editable=False, null=True)
  isArchived = models.BooleanField(default=False, blank=True)

  def save(self, *args, **kwargs):
    """ 
      Override On save method because we want to update the update date when we save this 
      kind of object
    """
    if self.id:
      # Write the update date automatically when we update the object
      self.updateDate = timezone.now()
    return super(RaceResult, self).save(*args, **kwargs)
  
  def __str__(self):
      return f"{self.raceId} - {self.name} ({self.year})"