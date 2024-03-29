from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from predictor.libs.processing import compose_the_base_df
from predictor.serializers.PredictorRequestSerializer import PredictorRequestSerializer, PredictorResponseSerializer


class PostPredictionRequest(APIView):
  def post(self, request):
    serializer = PredictorRequestSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      pred_request = serializer.save()
      # TODO Récupere les datas pour la prédiction ici
      response_data = compose_the_base_df(pred_request.driverId, pred_request.constructorId, 
                                          pred_request.circuitId, pred_request.raceRound, 
                                          pred_request.year)
      print(response_data)
      if 7200 == response_data["statusCode"]:
        pass
      else:
        res = {
          "statusCode": response_data["statusCode"],
          "message": response_data["message"],
        }
        pred_request.status = 'Fail'
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
      # Create data object to save in the database
      answerSerialiser = PredictorResponseSerializer(pred_request, context={"request": request})

      # if answerSerialiser.is_valid(raise_exception=True):
      return Response(answerSerialiser.data, status=status.HTTP_201_CREATED)
      # else:
      #   return Response(answerSerialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)