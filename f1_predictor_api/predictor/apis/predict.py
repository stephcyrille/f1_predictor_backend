import os
import pickle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from predictor.libs.processing import compose_prediction_df, compose_the_base_df, make_a_prediction, prepare_the_prediction
from predictor.serializers.PredictorRequestSerializer import PredictorRequestSerializer, PredictorResponseSerializer

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'mdel/modelv01.pkl')


class PostPredictionRequest(APIView):
  def post(self, request):
    # Check if the file exists
    if os.path.exists(MODEL_PATH):
      # Open the file and read its contents
      with open(MODEL_PATH, "rb") as f:
        loaded_model = pickle.load(f)
    
      serializer = PredictorRequestSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
        pred_request = serializer.save()
        # TODO Récupere les datas pour la prédiction ici
        response_data = compose_the_base_df(pred_request.driverId, pred_request.constructorId, 
                                            pred_request.circuitId, pred_request.raceRound, 
                                            pred_request.year)
        if 7200 == response_data["statusCode"]:
          # Create data object to save in the database
          prediction_df = compose_prediction_df(response_data['extra'])
          if 44 != len(prediction_df.columns):
            res = {
              "statusCode": response_data["statusCode"],
              "message": "The length of the dataframe doesn't match with the excpected size.",
            }
            pred_request.status = 'Fail'
            pred_request.errorMessage = res["message"]
            pred_request.save()
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

          df = prepare_the_prediction(prediction_df)
          if (0, 30) != (0, len(df.columns)):
            res = {
              "statusCode": response_data["statusCode"],
              "message": "The dataset lenght for this prediction must be (0, 30)",
            }
            pred_request.status = 'Fail'
            pred_request.errorMessage = res["message"]
            pred_request.save()
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
          
          race_rank = make_a_prediction(df, loaded_model)
          if 99 == race_rank:
            res = {
              "statusCode": response_data["statusCode"],
              "message": "Seems that we have a problem with the model prediction",
            }
            pred_request.status = 'Faif'
            pred_request.errorMessage = res["message"]
            pred_request.save()

          pred_request.status = 'Success'
          pred_request.predicted_rank = (race_rank + 1)
          pred_request.save()
          answerSerialiser = PredictorResponseSerializer(pred_request, context={"request": request})
          return Response(answerSerialiser.data, status=status.HTTP_201_CREATED)
        else:
          res = {
            "statusCode": response_data["statusCode"],
            "message": response_data["message"],
          }
          pred_request.status = 'Fail'
          pred_request.errorMessage = response_data["message"]
          pred_request.save()
          return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
      res = {
        "statusCode": '0000',
        "message": "We doesn't find the model",
      }
      return Response(res, status=status.HTTP_400_BAD_REQUEST)