from rest_framework import serializers
from predictor.models import PredictorRequest


class PredictorRequestSerializer(serializers.ModelSerializer):
  class Meta:
    model = PredictorRequest
    exclude = ["id"]

class PredictorResponseSerializer(serializers.Serializer):
  pass