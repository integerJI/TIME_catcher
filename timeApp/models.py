from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Timesave(models.Model):
    objects = models.Manager()
    save_user = models.ForeignKey(User, on_delete = models.CASCADE)
    save_date = models.IntegerField(default=0)
    input_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.save_user, self.save_date) 

