from rest_framework import serializers
from predictor.models import PredictorRequest


class PredictorRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = PredictorRequest
    exclude = ["id"]

class PredictorResponseSerializer(serializers.Serializer):
  race_rank = serializers.IntegerField(required=True)
  driverId = serializers.IntegerField(required=True)
  circuitId = serializers.IntegerField(required=True)

  def create(self):
    return ""

  def update(self):
    return ""
