from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'



class PostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post'


class ReviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'review'