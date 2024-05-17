from rest_framework import serializers
from circuits.models import Circuit
from drivers.models import Driver
from predictor.models import PredictorRequest
from drivers.serializers.DriverSerializer import DriverDetailSerializer

def get_upload_host(request):
  return "{0}://{1}".format(request.scheme, request.get_host())

class PredictorRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = PredictorRequest
    exclude = ["id"]

class PredictorResponseSerializer(serializers.ModelSerializer):
  driver_img = serializers.SerializerMethodField()
  driver_name = serializers.SerializerMethodField()
  circuit_name = serializers.SerializerMethodField()
  constructor_img = serializers.SerializerMethodField()

  def get_driver_img(self, instance):
    # TODO add a dumy image istead of an empty string
    try:
      driver = Driver.objects.get(driverId=instance.driverId)
      driver_img = get_upload_host(self.context["request"]) + driver.picture.url
    except:
       driver_img = ''
    return driver_img

  def get_constructor_img(self, instance):
    # TODO add a dumy image istead of an empty string
    try:
      driver = Driver.objects.get(driverId=instance.driverId)
      constructor_img = get_upload_host(self.context["request"]) + driver.constructorId.logo.url
    except:
      constructor_img = ''
    return constructor_img
  
  def get_driver_name(self, instance):
    try:
      driver = Driver.objects.get(driverId=instance.driverId)
      driver_name = driver.full_name
    except Exception as e:
      # TODO add logger to get the error here
      driver_name = ''
    return driver_name

  def get_circuit_name(self, instance):
    try:
      circuit = Circuit.objects.get(circuitId=instance.circuitId)
      circuit_name = circuit.name
    except Exception as e:
      # TODO add logger to get the error here
      circuit_name = ''
    return circuit_name

  class Meta:
    model = PredictorRequest
    fields = ["driver_img", "driver_name", "circuit_name", "constructor_img", "predicted_rank"]