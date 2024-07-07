
from utils.sentiment_analyzer import ChatGPTSentimentAnalyzer
from aquarius.models import Post, City, Comment, Report, HotTopic
from aquarius.serializers import PostSerializer, CommentSerializer, ReportSerializer
import random
from django.db.models import Count
class RedditService:
            
    def generate_report(self, post_id):
        report = Report.objects.filter(post_id=post_id)
        if report.exists():
            return report.first()

        comments = Comment.objects.select_related('post').filter(post_id=post_id)
        classified_comments = {'in_favor': [], 'against': [], 'neutral': []}
        for comment in comments:
            post = comment.post
            category, reason = ChatGPTSentimentAnalyzer().classify_comments(comment.post, comment.topic)
            comment.classification = category
            comment.description = reason
            comment.save()
            if category == 'in favor':
                classified_comments['in_favor'].append(comment)
            elif category == 'against':
                classified_comments['against'].append(comment)
            else:
                classified_comments['neutral'].append(comment)

            report, created = Report.objects.get_or_create(post=post)
            report.favour = len(classified_comments['in_favor'])
            report.against = len(classified_comments['against'])
            report.neutral = len(classified_comments['neutral'])
            report.save()

        return report


    def get_random_post(self, city):
        report = [] # Report.objects.filter(against__gte=5).values_list('post_id', flat=True)
        filter= {"city__name": city}
        if len(report) > 0:
            filter["id__in"] = report
        posts_count = Post.objects.filter(**filter).count()
        if posts_count == 0:
            return None
        random_index = random.randint(0, posts_count - 1)
        post = Post.objects.filter(city__name=city)[random_index]
        return post

    def get_summary(self, post_id):
        post = Post.objects.get(id=post_id)
        report = self.generate_report(post.id)
        return {
            "comments": Comment.objects.filter(post=post), 
            "summary": ReportSerializer(report).data, 
            "post": PostSerializer(post).data,
        }
    
    def summarize_results(self, classified_comments):
        summary = {
            'in_favor': {'total': 0, 'arguments': {}},
            'against': {'total': 0, 'arguments': {}},
            'neutral': 0
        }



        # In favor comments
        in_favor_comments = classified_comments['in_favor']
        summary['in_favor']['total'] = len(in_favor_comments)

        # Against comments
        against_comments = classified_comments['against']
        summary['against']['total'] = len(against_comments)

        # Neutral comments
        summary['neutral'] = len(classified_comments['neutral'])

        return summary