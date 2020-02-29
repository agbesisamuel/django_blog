from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #allow us to get the absolute url, and send the user to the post detail page, after user create a new post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


