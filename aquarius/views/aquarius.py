from rest_framework.generics import ListAPIView
from aquarius.models import City, Post
from aquarius.serializers import CitySerializer
from django.contrib.auth.models import User, Group
from aquarius.service import PostService
from django.shortcuts import render
from aquarius.service import RedditService

class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

def reddit_summary_view(request, city):
    service = PostService()
    result = service.fetch_posts(city)
    return render(request, 'summary.html', {**result})


def post_summary(request, post_id):
    summary_details = RedditService().get_summary(post_id)
    return render(request, 'admin/summary.html', summary_details)