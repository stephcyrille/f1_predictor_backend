from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from circuits.apis.circuit_apis import AllCircuitsAPIView

urlpatterns = [
  path('all/', AllCircuitsAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)