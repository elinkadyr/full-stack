from django.db import models

from account.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Like(models.Model):
    user = models.ForeignKey(MyUser, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(MyUser, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)