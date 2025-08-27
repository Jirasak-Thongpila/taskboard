from django.db import models
from django.contrib.auth import get_user_model

class Task(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    detail = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title
