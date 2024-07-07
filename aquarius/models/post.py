from django.db import models
class Post(models.Model):
    topic = models.TextField()
    content = models.TextField(default='')
    source = models.CharField(max_length=100)
    total_comments = models.IntegerField(default=0)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f"{self.id}"
    
class Comment(models.Model):
    topic = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    classification = models.CharField(max_length=10, choices=[('in_favor', 'in_favor'), ('against', 'against'), ('neutral', 'neutral')])
    description = models.TextField(default='')

    def __str__(self):
        return f"{self.id}"

    
class Report(models.Model):
    favour = models.IntegerField(default=0)
    against = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')

    def __str__(self):
        return f"{self.post_id}"


class Arguments(models.Model):
    topic = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name="arguments")
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, related_name="arguments")

    def __str__(self):
        return f"{self.post_id} - {self.comment_id}"

class HotTopic(models.Model):
    topic = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='hot_topics')
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='hot_topics')

    def __str__(self):
        return f"{self.topic}"
