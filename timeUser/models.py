# myProject/myMember/models.py

from django.db import models
from django.contrib.auth.models import User
from betterforms.multiform import MultiModelForm
from django import forms

class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'
        
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick = models.CharField(verbose_name='NickName', max_length=50, blank=True,)
    intro = models.TextField(blank=True, max_length=200, )
    birth_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nick
