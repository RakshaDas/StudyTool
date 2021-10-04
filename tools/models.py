from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User


# Create your models here.

class Notes(models.Model):
    title = models.CharField(max_length=500, null=False)
    content = HTMLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Todo(models.Model):
    task = models.CharField(max_length=500, null=False)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task
