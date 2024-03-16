from rest_framework.response import Response
from rest_framework.views import APIView
from drivers.models import Driver
from drivers.serializers.DriverSerializer import DriverDetailSerializer


class AllDriversAPIView(APIView):
  queryset = Driver.objects.none()
  serializer_class = DriverDetailSerializer

  def get_queryset(self):
    return Driver.objects.filter(driver_is_active=1, isArchived=False)

  def get(self, request):
    queryset = self.get_queryset()
    serializer = DriverDetailSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data)