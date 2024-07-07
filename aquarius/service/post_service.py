
from aquarius.models import City, Post, HotTopic, Comment
from aquarius.serializers import PostSerializer, HotTopicSerializer
from utils.sentiment_analyzer import ChatGPTSentimentAnalyzer
from utils.social_sites.reddit import RedditAPI

class PostService:

    def fetch_posts(self, city_name):
        posts = RedditAPI().fetch_hot_posts(city_name)
        city, created = City.objects.get_or_create(name=city_name)
        result = {"post_count": 0, "comment_count": 0}
        for post in posts:
            new_post, created = Post.objects.get_or_create(topic=post.title, city=city)
            if created:
                new_post.content = post.selftext
                new_post.source = 'reddit'
                new_post.save()
                post.comments.replace_more(limit=0)
                comments = [] 
                for comment in post.comments.list():
                    if hasattr(comment, 'body'):
                        comments.append(Comment(topic=comment.body, post=new_post))

                Comment.objects.bulk_create(comments)
                new_post.total_comments = len(comments)
                new_post.save()
                result["post_count"] += 1
                result["comment_count"] += len(comments)

        return result

    def get_posts_by_city(self, city_id, topic='', generate=None):
        filter = {'city': city_id}
        if topic:
            post_ids = HotTopic.objects.filter(topic=topic).values_list('post_id', flat=True)
            filter['id__in'] = post_ids
        
        if generate == 'posts':
            city = City.objects.get(id=city_id)
            self.fetch_posts(city.name)
        if generate == 'hot-topics':
            self.generate_hot_topics(city_id)

        posts = Post.objects.filter(**filter)
        hot_topics = HotTopic.objects.filter(city=city_id).values('topic').distinct()
        return {
            "posts": PostSerializer(posts, many=True).data, 
            "hot_topics": HotTopicSerializer(hot_topics, many=True).data
        }

    def get_summary(self, post_id):
        pass
    
    def generate_hot_topics(self, city_id):
        city = City.objects.get(id=city_id)
        posts = Post.objects.filter(city_id=city_id)
        result = ChatGPTSentimentAnalyzer().get_hot_topics(city.name, posts)
        hot_topics = []
        for topic, posts in result.items():
            for post_id in posts:
                hot_topics.append(HotTopic(topic=topic, post_id=post_id, city_id=city_id))

        HotTopic.objects.bulk_create(hot_topics)

    
    def identify_arguments(self, post_id):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post_id=post_id, classification='in favor')
        result = ChatGPTSentimentAnalyzer().identify_arguments(post, comments)


        arguments = {}
        for comment in comments:
            doc = comment
            if doc in arguments:
                arguments[doc].append(comment)
            else:
                arguments[doc] = [comment]
        return arguments