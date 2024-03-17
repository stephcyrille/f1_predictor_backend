from rest_framework.response import Response
from rest_framework.views import APIView
from circuits.models import Circuit
from circuits.serializers.CircuitSerializer import CircuitDetailSerializer


class AllCircuitsAPIView(APIView):
  queryset = Circuit.objects.none()
  serializer_class = CircuitDetailSerializer

  def get_queryset(self):
    return Circuit.objects.filter(circuits_is_active=1, isArchived=False)

  def get(self, request):
    queryset = self.get_queryset()
    serializer = CircuitDetailSerializer(queryset, many=True, context={"request": request})
    return Response(serializer.data)