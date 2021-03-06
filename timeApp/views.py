from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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
from datetime import datetime
from django.utils.dateformat import DateFormat

def index(request):
    return render(request, 'index.html')

# 시간 저장
@login_required
@require_POST
def timesave(request):
    if request.method == 'POST':
        timesave = Timesave()
        timesave.save_user = User.objects.get(username = request.user.get_username())
        timesave.save_date = request.POST.get('time')
        timesave.input_date = DateFormat(datetime.now()).format('Ymd')
        timesave.save()
        return HttpResponse(content_type='application/json')

def calender(request):
    return render(request, 'calender.html')

def mobile(request):
    return render(request, 'mobile.html')

# 공지사항 리스트 호출
def notices(request):
    notices = Notices.objects.all().order_by('-id')

    paginator = Paginator(notices,10)
    page = request.GET.get('page')
    notices_posts = paginator.get_page(page)

    conn_user = request.user # 현재 접속중인 user 정보를 가져와 conn_user에 넣는다.
    conn_profile = Profile.objects.get(user=conn_user) # Profile DB에서 접속 유저와 같은 데이터를 가져온다.

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'notices' : notices,
        'notices_posts' : notices_posts,
    }

    return render(request, 'notices.html', context=context)

# 공지사항 글 쓰기 페이지 호출
def notices_create(request):
    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }

    return render(request, 'notices_create.html', context=context)

# 공지사항 글 쓰기 
def notices_save(request):
    notices = Notices()

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }

    notices.n_user = User.objects.get(username = request.user.get_username())
    notices.n_title = request.POST['title']
    notices.n_body = request.POST['body']
    notices.n_input_date = timezone.datetime.now()
    notices.save()
    
    return redirect('/timeApp/notices_detail/' + str(notices.id), context=context)

def notices_detail(request, notice_id):
    notices = get_object_or_404(Notices, pk=notice_id)

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'notices' : notices,
    }

    return render(request, 'notices_detail.html', context=context)

def notices_update(request, notice_id):
    notices = Notices.objects.get(pk=notice_id)

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
    }

    if request.method == "POST":
        notices.n_user = User.objects.get(username = request.user.get_username())
        notices.n_title = request.POST['title']
        notices.n_body = request.POST['body']
        notices.n_input_date = timezone.datetime.now()
        notices.save()
        return redirect('/timeApp/notices_detail/' + str(notices.id), context=context)
    else :
        return render(request, 'notices_update.html', context=context)

def notices_delete(request, notice_id):
    notices = Notices.objects.get(pk=notice_id)
    notices.delete()
    return redirect('/timeApp/notices/')

def customer(request):    
    customers = Customer.objects.all().order_by('-id')

    paginator = Paginator(customers,10)
    page = request.GET.get('page')
    customers_posts = paginator.get_page(page)

    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'customers' : customers,
        'customers_posts' : customers_posts,
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

    customer.c_user = User.objects.get(username = request.user.get_username())
    customer.c_title = request.POST['title']
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
        customer.c_user = User.objects.get(username = request.user.get_username())
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
