from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="likes")
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def like_count(self):
        return self.like.all().count()

    @property
    def post_comments(self):
        return self.comments_set.all()


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment
