from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from .models import Timesave
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

@login_required
@require_POST
def timesave(request):
    if request.method == 'POST':
        
        timesave = Timesave()
        timesave.save_user = User.objects.get(username = request.user.get_username())
        timesave.save_date = request.POST.get('time')
        timesave.save()

        return HttpResponse(content_type='application/json')
