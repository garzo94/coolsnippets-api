from django.db import models
from django.conf import settings

# Create your models here.
class Language(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=75)

class Topic(models.Model):

    name = models.CharField(max_length=100)
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,

    )

class Subtopic(models.Model):
     name = models.CharField(max_length=100)
     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')

class Snipped(models.Model):
    title = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=50)
    background = models.IntegerField(default=0)
    highlighted = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    twitter = models.BooleanField(default=False)



class Twitter(models.Model):
    name = models.CharField(max_length=100)
    alias = models.TextField(max_length=50)
    image = models.CharField(max_length=50)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
