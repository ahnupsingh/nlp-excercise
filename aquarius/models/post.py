from django.db import models
class Post(models.Model):
    topic = models.TextField()
    source = models.CharField(max_length=100)
    total_comments = models.IntegerField(default=0)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    topic = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name

    
class Report(models.Model):
    favour = models.IntegerField(default=0)
    against = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')

    def __str__(self):
        return self.post_id


class Arguments(models.Model):
    topic = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name="arguments")
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, related_name="arguments")

    def __str__(self):
        return f"{self.post_id} - {self.comment_id}"
