from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
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

def mobile(request):
    return render(request, 'mobile.html')




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



def notices_create(request):

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }

    return render(request, 'notices_create.html', context=context)

def notices_detail(request, notices_id):

    notices = get_object_or_404(Notices, pk=notices_id)

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'notices' : notices,
    }

    return render(request, 'notices_detail.html', context=context)




# 건의사항 소스 시작
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

def customer_detail(request, customer_id):

    customers = get_object_or_404(Customer, pk=customer_id)

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'customers' : customers,
    }

    return render(request, 'customer_detail.html', context=context)

def customer_create(request):

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }
    
    return render(request, 'customer_create.html', context=context)

def customer_save(request):

    customer = Customer()
    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }

    customer.c_title = request.POST['title']
    customer.c_body = request.POST['body']
    customer.c_input_date = timezone.datetime.now()
    customer.save()
    
    return redirect('/timeApp/customer_detail/' + str(customer.id), context=context)



def customer_update(request, customers_id):
    customers = Customer.objects.get(pk=customers_id)

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }

    if request.method == "POST":
        customers.c_title = request.POST['title']
        customers.c_body = request.POST['body']
        customers.c_input_date = timezone.datetime.now()
        customers.save()
        return redirect('/timeApp/customer_detail/' + str(customers.id), context=context)

    else :
        return render(request, 'customer_update.html', context=context)

def customer_delete(request, customers_id):
    customers = Customer.objects.get(pk=customers_id)
    customers.delete()
    return redirect('/timeApp/customer/')


