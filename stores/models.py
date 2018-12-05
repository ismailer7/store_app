from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=120)
    distance = models.IntegerField(default=0)
    users = models.ManyToManyField(User, related_name='stores')
    is_preffered = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return '{0} store away by {1} meters'.format(self.name, self.distance, self.is_preffered, self.date)