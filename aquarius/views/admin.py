from aquarius.models import City, Post, Comment, Report
from django.contrib.auth.models import User, Group
from aquarius.service import ChartService, RedditService

def dashboard_callback(request, context):
    bar_chart_details = ChartService().bar_chart()
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
            "cities": City.objects.all(),
            "scripts": ["/static/admin_dashboard.js"],
            **bar_chart_details,
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

def post_badge_callback(request):
    return Post.objects.count()

def comment_badge_callback(request):
    return Comment.objects.count()

def report_badge_callback(request):
    return Report.objects.count()