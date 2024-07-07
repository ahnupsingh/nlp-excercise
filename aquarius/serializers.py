from rest_framework import serializers
from .models import City, Post, Comment, Report, HotTopic

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):

    city = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['topic', 'content', 'city', 'id', 'source', 'total_comments']

    def get_city(self, obj):
        return obj.city.name

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['topic']

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['favour', 'against', 'neutral', 'post_id']

class HotTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotTopic
        fields = ['topic', 'post_id',]