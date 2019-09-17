from django.db import models
from django.conf import settings


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    color = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)


    def __str__(self):
        return self.title