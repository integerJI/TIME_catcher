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

class Notices(models.Model):
    objects = models.Manager()
    n_title = models.CharField(max_length=100)
    n_body = models.TextField()
    n_hit = models.PositiveIntegerField(default=0)
    n_input_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.n_title

    @property
    def update_counter(self):
        self.n_hit = self.n_hit + 1
        self.save()
