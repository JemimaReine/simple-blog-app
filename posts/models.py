from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.utils.timezone import now
# Create your models here.

class User(AbstractUser):
    pass
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")
    title = models.CharField(max_length=165)
    body = HTMLField()
    image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(default=now, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_dislikes')
    like = models.BooleanField(default=False)  # True for like, False for dislike

    def __str__(self):
        return f"{self.user.username} {'liked' if self.like else 'disliked'} {self.post.title}"

