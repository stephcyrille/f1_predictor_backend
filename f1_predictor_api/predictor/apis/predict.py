from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from predictor.models import PredictorRequest
from predictor.serializers.PredictorRequestSerializer import PredictorRequestSerializer, PredictorResponseSerializer


class PostPredictionRequest(APIView):
  def post(self, request):
    serializer = PredictorRequestSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      # Create data object to save in the database
      # serializer.save()
      print(serializer.data)
      driver = serializer.data['driverId']
      circuit = serializer.data['circuitId']
      res = {
        'race_rank': 4,
        'driverId': driver,
        'circuitId': circuit,
      }
      answerSerialiser = PredictorResponseSerializer(data=res)

      if answerSerialiser.is_valid(raise_exception=True):
        return Response(answerSerialiser.data, status=status.HTTP_201_CREATED)
      else:
        return Response(answerSerialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)