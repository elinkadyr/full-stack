from django.db import models

from account.models import MyUser


"""модель для постов"""
class Post(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} -> {self.title}"


"""модель для комментариев на посты"""
class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"post <{self.post.title}> commented by <{self.user.email}>"


"""модель для лайков на посты"""
class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"post <{self.post.title}> liked by <{self.user.email}>"
    

"""модель для избранного для постов"""
class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='post_favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_favorites')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'<{self.post.title}> added to favorites by {self.user.email}'