from rest_framework.generics import ListAPIView
from aquarius.models import City
from aquarius.serializers import CitySerializer
from django.contrib.auth.models import User, Group
from aquarius.service import RedditService
from django.shortcuts import render

class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

def reddit_summary_view(request, topic):
    service = RedditService()
    result = service.fetch_hot_posts(topic)
    return render(request, 'summary.html', {**result, 'topic': topic})