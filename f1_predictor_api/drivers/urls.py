from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from drivers.apis.drivers_apis import AllDriversAPIView

urlpatterns = [
  path('all/', AllDriversAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)