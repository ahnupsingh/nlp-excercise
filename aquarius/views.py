from rest_framework.generics import ListAPIView
from .models import City
from .serializers import CitySerializer

class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer