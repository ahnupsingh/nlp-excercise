from aquarius.models import City
from django.contrib.auth.models import User, Group
from aquarius.service import ChartService, RedditService

def dashboard_callback(request, context):
    bar_chart_details = ChartService().bar_chart()
    topic = "kathmandu"
    summary_details = RedditService().fetch_hot_posts(topic)
    context.update(
        {
            "cards": [
                {
                    "title": "Total Posts", 
                    "metric": "100"
                },
                {
                    "title": "Total Comments", 
                    "metric": "100"
                },
                {
                    "title": "Total Analysis", 
                    "metric": "100"
                },
            ],
            **bar_chart_details,
            **summary_details, 
            'topic': topic
        }
    )
    return context

def city_badge_callback(request):
    return City.objects.count()

def user_badge_callback(request):
    return User.objects.count()

def group_badge_callback(request):
    return Group.objects.count()

def report_badge_callback(request):
    return 0
