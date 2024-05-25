from django.db import models
from django.utils import timezone
from django.utils.text import slugify

def circuit_path(instance, filename):
  circuit_slug = slugify(instance.name)
  return f"circuits/{circuit_slug}/track/{filename}"

def circuit_card_path(instance, filename):
  circuit_slug = slugify(instance.name)
  return f"circuits/{circuit_slug}/card/{filename}"

def circuit_country_path(instance, filename):
  circuit_slug = slugify(instance.name)
  return f"circuits/{circuit_slug}/flag/{filename}"

class Circuit(models.Model):
  circuitId = models.IntegerField('Circuit ID', unique=True)
  name = models.CharField('Circuit Name', max_length=100)
  location = models.CharField('Location', max_length=100)
  country = models.CharField('Country', max_length=100)
  lat = models.DecimalField('Latitude', max_digits=10, decimal_places=2)
  lng = models.DecimalField('Longitude', max_digits=10, decimal_places=2)
  circuits_is_active = models.IntegerField('Is active')
  createdDate = models.DateTimeField(blank=True, editable=False, default=timezone.now)
  updateDate = models.DateTimeField(blank=True, editable=False, null=True)
  isArchived = models.BooleanField(default=False, blank=True)
  picture = models.FileField(upload_to=circuit_path, null=True, blank=True)
  card_img = models.FileField(upload_to=circuit_card_path, null=True, blank=True)
  country_img = models.FileField(upload_to=circuit_country_path, null=True, blank=True)
  raceRound = models.CharField('Round', max_length=2, blank=True, null=True)

  def save(self, *args, **kwargs):
    """ 
      Override On save method because we want to update the update date when we save this 
      kind of object
    """
    if self.id:
      # Write the update date automatically when we update the object
      self.updateDate = timezone.now()
    return super(Circuit, self).save(*args, **kwargs)
  
  def __str__(self):
      return self.name