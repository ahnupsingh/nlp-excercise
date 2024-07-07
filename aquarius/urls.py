from django.urls import path
from .views import CityListView, reddit_summary_view, posts_by_city, post_summary

app_name = 'aquarius'

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city-list'),
    path('reddit_summary/<str:city>/', reddit_summary_view, name="reddit_summary"),
    path('posts_by_city/<int:city_id>/', posts_by_city, name='posts_by_city'),
    path('post_summary/<int:post_id>/', post_summary, name='post_summary'),
]