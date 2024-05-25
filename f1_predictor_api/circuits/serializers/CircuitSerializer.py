from rest_framework import serializers
from circuits.models import Circuit

def get_upload_host(request):
    return "{0}://{1}".format(request.scheme, request.get_host())


class CircuitDetailSerializer(serializers.ModelSerializer):
  circuit_img = serializers.SerializerMethodField()
  card_img = serializers.SerializerMethodField()
  country_img = serializers.SerializerMethodField()
  round = serializers.SerializerMethodField()

  def get_circuit_img(self, instance):
      # TODO add a dumy image istead of an empty string
      try:
        circuit_img = get_upload_host(self.context["request"]) + instance.picture.url
      except:
        circuit_img = ''
      return circuit_img

  def get_card_img(self, instance):
      # TODO add a dumy image istead of an empty string
      try:
        card_img = get_upload_host(self.context["request"]) + instance.card_img.url
      except:
         card_img = ''
      return card_img

  def get_country_img(self, instance):
      # TODO add a dumy image istead of an empty string
      try:
        country_img = get_upload_host(self.context["request"]) + instance.country_img.url
      except:
         country_img = ''
      return country_img
  
  def get_round(self, instance):
      return instance.raceRound

  class Meta:
    model = Circuit
    fields = ['circuitId', 'name', 'location', 'country', 'circuit_img', 'card_img', 'country_img', 'round']