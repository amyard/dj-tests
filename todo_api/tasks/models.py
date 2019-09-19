from django.db import models
from django.conf import settings
from django.utils.text import slugify
from model_utils.models import TimeStampedModel


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, null=True)
    color = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.user.username}'

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.title), slugify(self.user.username)))
        super(Project, self).save(*args, **kwargs)




class Task(TimeStampedModel):

    HIGN = 1
    MIDDLE = 0
    LOW = -1
    PRIORITY = ((HIGN, 'Hign'),(MIDDLE, 'Middle'),(LOW, 'Low'))

    COMPLETED = 1
    UNCOMPLETED = 0
    STATUS = ((COMPLETED, 'Completed'),(UNCOMPLETED, 'Uncompleted'))

    project = models.ForeignKey('Project', on_delete = models.CASCADE, related_name = 'project')
    title = models.CharField(max_length = 255)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    description = models.TextField(blank=True, null=True, default='')
    priority = models.IntegerField(choices=PRIORITY, default = HIGN)
    status = models.IntegerField(choices = STATUS, default = UNCOMPLETED)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.title), slugify(self.project.user.username)))
        super(Task, self).save(*args, **kwargs)