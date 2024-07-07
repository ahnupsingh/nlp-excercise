from aquarius.service import PostService
from django.http import JsonResponse

def posts_by_city(request, city_id):
    topic = request.GET.get('topic', None)
    generate = request.GET.get('generate', None)
    result = PostService().get_posts_by_city(city_id, topic, generate)
    return JsonResponse(result, safe=False)