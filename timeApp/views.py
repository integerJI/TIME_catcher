from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.models import User
from .models import Timesave, Notices, Customer
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum
from timeUser.models import Profile

def index(request):
    return render(request, 'index.html')

@login_required
@require_POST
def timesave(request):
    if request.method == 'POST':
        
        timesave = Timesave()
        timesave.save_user = User.objects.get(username = request.user.get_username())
        
        timesave.save_date = request.POST.get('time')
        timesave.save()

        return HttpResponse(content_type='application/json')

def calender(request):
    return render(request, 'calender.html')

def notices(request):
    
    notices = Notices.objects.all().order_by('-id')

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'notices' : notices,
    }

    return render(request, 'notices.html', context=context)


def customer(request):
    
    customers = Customer.objects.all().order_by('-id')

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'customers' : customers,
    }

    return render(request, 'customer.html', context=context)



    