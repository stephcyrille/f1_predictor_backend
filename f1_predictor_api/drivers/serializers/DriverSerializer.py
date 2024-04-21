from rest_framework import serializers
from drivers.models import Driver

def get_upload_host(request):
    return "{0}://{1}".format(request.scheme, request.get_host())


class DriverDetailSerializer(serializers.ModelSerializer):
  driver_img = serializers.SerializerMethodField()
  constructor_img = serializers.SerializerMethodField()

  def get_driver_img(self, instance):
    # TODO add a dumy image istead of an empty string
    try:
      driver_img = get_upload_host(self.context["request"]) + instance.picture.url
    except:
       driver_img = ''
    return driver_img

  def get_constructor_img(self, instance):
    # TODO add a dumy image istead of an empty string
    try:
      constructor_img = get_upload_host(self.context["request"]) + instance.constructorId.logo.url
    except:
      constructor_img = ''
    return constructor_img

  class Meta:
    model = Driver
    fields = ['driverId', 'constructorId', 'full_name', 'number', 'nationality', 'driver_img', 'constructor_img']