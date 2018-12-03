from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=120)
    distance = models.IntegerField(default=0)
    users = models.ManyToManyField(User, related_name='stores')
    is_preffered = models.BooleanField(default=False)

    def __str__(self):
        return '{0} - {1} store by {2} meters , isPreffered : {3}'.format(self.id, self.name, self.distance, self.is_preffered)