from django.db import models
from django.conf import settings

def user_directory_path(instance,filename):
    return 'image/{0}'.format(filename)


class Language(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

    @property
    def topic(self):#topics to read in my nested serailizer
        return self.topic_set.all()

class Topic(models.Model):
    name = models.CharField(max_length=100)
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
    )

class Subtopic(models.Model):
     name = models.CharField(max_length=100)
     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics', null=True)

class Snipped(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    xtitle =models.DecimalField(max_digits=8, decimal_places=5,blank=True, null=True)
    ytitle =models.DecimalField(max_digits=8, decimal_places=5,blank=True,null=True)
    text = models.CharField(max_length=300, blank=True, null=True)
    xtext =models.DecimalField(max_digits=8, decimal_places=5,blank=True,null=True)
    ytext =models.DecimalField(max_digits=8, decimal_places=5,blank=True,null=True)
    background = models.IntegerField(default=0)
    code = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, default='snippets/default.jpg')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE,null=True, blank=True)
    twitter = models.CharField(max_length=100,default="",null=True, blank=True)





