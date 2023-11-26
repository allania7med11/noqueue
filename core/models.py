from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User 


class Queue(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class QueueCitation(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    number = models.IntegerField()
    state_choices = [
        ('NS', 'Not Served'),
        ('SV', 'Served'),
    ]
    state = models.CharField(max_length=2, choices=state_choices)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.queue} - {self.number} ({self.get_state_display()})"
