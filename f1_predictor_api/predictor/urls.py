from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from predictor.apis.predict import PostPredictionRequest

urlpatterns = [
  path('post/', PostPredictionRequest.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)