from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    def __str__(self):
        return '{}'.format(self.username)

    def posts(self):
        return self.post_set.all().order_by('-time')


class Profile(models.Model):
    def __str__(self):
        return '{}\'s profile'.format(self.user)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_user.jpg', upload_to='profile_pics')
    followed = models.ManyToManyField(User, related_name='followers', blank=True)
    joined = models.DateTimeField(default=timezone.now)

    def follows_count(self):
        return len(self.followed.all())

    def followers_count(self):
        return len(self.user.followers.all())

class Post(models.Model):
    def __str__(self):
        return 'at {} {} wrote: {}'.format(self.time, self.author, self.content)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked', blank=True)

    class Meta:
        ordering = ['-time']

    def likes_count(self):
        return len(self.likes.all())

class CommentPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
