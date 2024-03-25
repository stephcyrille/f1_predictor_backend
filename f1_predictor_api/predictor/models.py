from django.db import models
from django.utils import timezone
import math
from django.db.models.signals import post_save

class PredictorRequest(models.Model):
  ref = models.CharField('Reference', max_length=21, editable=False, blank=False, unique=True)
  driverId = models.IntegerField('Driver ID', blank=False, null=False)
  constructorId = models.IntegerField('Constructor ID', blank=False, null=False)
  circuitId = models.IntegerField('Circuit Id', blank=False, null=False)
  raceRound = models.IntegerField('Race round', blank=False, null=False)
  year = models.IntegerField('Year', blank=False, null=False)
  status = models.CharField('Status', max_length=20, default='New')
  predicted_rank = models.CharField('Prediction', max_length=2, blank=True, null=True)
  createdDate = models.DateTimeField(blank=True, editable=False, default=timezone.now)
  updateDate = models.DateTimeField(blank=True, editable=False, null=True)
  isArchived = models.BooleanField(default=False, blank=True)

  def save(self, *args, **kwargs):
    """ 
      Override On save method
    """
    if self.id:
      # Write the update date automatically when we update the object
      self.updateDate = timezone.now()
    return super(PredictorRequest, self).save(*args, **kwargs)
    
  def __str__(self) -> str:
    return self.ref

def create_ref_receiver(sender, instance, **kwargs):
  if '' == instance.ref:
    month_digits = int(math.log10(timezone.now().month)) + 1
    day_digits = int(math.log10(timezone.now().day)) + 1
    month = timezone.now().month
    day = timezone.now().day
    if 1 == month_digits:
      month = f"0{timezone.now().month}"

    if 1 == day_digits:
      day = f"0{timezone.now().day}"

    prefix = f"PREQ/{timezone.now().year}/{month}/{day}/"

    nbr_of_zero = 5
    digits = int(math.log10(instance.id)) + 1
    nbr_of_zero -= digits
    surfix = f"{'0' * nbr_of_zero}{instance.id}"
    instance.ref = prefix + surfix
    instance.save()

post_save.connect(create_ref_receiver, sender= PredictorRequest)