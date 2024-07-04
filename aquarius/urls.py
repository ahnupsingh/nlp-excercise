from django.urls import path
from .views import CityListView, reddit_summary_view

app_name = 'aquarius'

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city-list'),
    path('reddit_summary/<str:topic>/', reddit_summary_view, name="reddit_summary"),
]