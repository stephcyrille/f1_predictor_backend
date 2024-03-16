from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def logo_path(instance, filename):
  constructor_slug = slugify(instance.constructor_name)
  return f"constructors/logos/{constructor_slug}"

class Constructor(models.Model):
  constructorId = models.IntegerField('Constructor ID', null=False)
  constructor_name = models.CharField('Name', max_length=80, null=False)
  constructor_country = models.CharField('Country', max_length=120, null=False)
  constructor_is_active = models.IntegerField('Is active', null=False)
  constructor_races_won = models.IntegerField('Number of races won', null=False)
  constructor_avg_point = models.DecimalField('Constructor AVG points', null=False, max_digits=10, decimal_places=2)
  constructor_times_in_top_10 = models.IntegerField('Number the time in the top 10', null=False)
  createdDate = models.DateTimeField(blank=True, editable=False, default=timezone.now)
  updateDate = models.DateTimeField(blank=True, editable=False, null=True)
  isArchived = models.BooleanField(default=False, blank=True)
  # TODO Add the picture of the constructor
  logo = models.FileField(upload_to=logo_path, null=True)

  def save(self, *args, **kwargs):
    """ 
      Override On save method because we want to update the update date when we save this 
      kind of object
    """
    if self.id:
      # Write the update date automatically when we update the object
      self.updateDate = timezone.now()
      return super(Constructor, self).save(*args, **kwargs)


