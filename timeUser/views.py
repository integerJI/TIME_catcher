from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from .forms import UserCreationMultiForm, ProfileForm, ProfileUpdateForm
from django.db.models import Sum
from .models import Profile
from timeApp.models import Timesave
from datetime import datetime
from django.utils.dateformat import DateFormat

# 회원가입 함수(api) 호출
def signup(request):
    form = UserCreationMultiForm(request.POST, request.FILES)
    if request.method == 'POST': # 메소드가 POST만 실행
        userCheck = request.POST['user-username'] # userCheck라는 변수에 request 받은 (html에서 user-username이라는 값)을 저장

        if len(request.POST['month']) < 2: # 이건 month(월)이 한자리일 경우 앞에 0을 붙이는 로직
            changeMonth = request.POST['month'].zfill(2)
        else:
            changeMonth=request.POST['month']

        if len(request.POST['day']) < 2: # 일도 마찬가지 Ex) '1' -> '01'
            changeDay = request.POST['day'].zfill(2)
        else:
            changeDay = request.POST['day']

        changeBirth = request.POST['year']+'-'+changeMonth+'-'+changeDay # 각각의 변수를 changeBirth 변수에 2020-08-01이라는 값으로 만들어서 저장

        if request.POST['user-password1'] == request.POST['user-password2']: # 비밀번호 1과 2를 비교해 같을 경우 다음 함수 실행
            if form.is_valid(): # form의 유효성 검사
                user = form['user'].save()
                profile = form['profile'].save(commit=False)
                profile.user = user
                profile.birth_date = changeBirth # 생일 값은 위에서 만들어준 changeBirth값
                profile.plan = request.POST['profile-plan'] # plan은 목표 시간
                profile.save() # 저장
                print('회원가입 성공') # 아래에 터미널 창에 회원가입 성공이라는 로그 출력
                return redirect('signin') # signin으로 redirect
            else:
                if User.objects.get(username=userCheck): # User DB에서 새로 들어오는 userCheck라는 값이 있는지 비교
                    print('아이디 중복')
                    messages.info(request, '아이디가 중복됩니다.') # 맞을경우 messages에 안내 문구를 넣어 반환
                    return render(request, 'signup.html') # 다시 회원가입 페이지로
                print('회원가입 실패') 
                messages.info(request, '회원가입에 실패했습니다.') # user체크에 실패했을 경우 안내문구 출력
                return render(request, 'signup.html')
        else: # 위에서 보면 비밀번호 1과 2를 비교하는 부분의 else
            print('비밀번호가 달라서 실패')
            messages.info(request, '비밀번호가 다릅니다.') # 여기로 온건 비밀번호 1과 2가 달라서 실패
            return render(request, 'signup.html')

    return render(request, 'signup.html', { "form": form }) # form 부분은 django form 검색 해보기

class Loginviews(LoginView): # django에서 제공해주는 Login 함수
    template_name = 'signin.html'

    def form_invalid(self, form):
        messages.error(self.request, '로그인에 실패하였습니다. Id 혹은 Password를 확인해 주세요.', extra_tags='danger')
        return super().form_invalid(form)

signin = Loginviews.as_view()

class LogoutViews(LogoutView): # 마찬가지로 django에서 제공
    # setting.py에 설정해준 값
    next_page = settings.LOGOUT_REDIRECT_URL
signout = LogoutViews.as_view()

@login_required
def userinfo(request): # mypage 시작
    today = DateFormat(datetime.now()).format('Ymd') # 현재 시간을 Ymd 포멧으로 today에 저장 Ex) 2020-08-01

    conn_user = request.user # 현재 접속중인 유저를 conn_user에 저장
    conn_profile = Profile.objects.get(user=conn_user) # Profile models에서 현재 접속중인 유저의 정보를 conn_porfile에 저장

    timesave = Timesave.objects.filter(input_date=today, save_user_id=conn_user) # Timesave models에서 그리고 현재 접속중인 유져의 today값을 가져옴
    sum = Timesave.objects.filter(input_date=today, save_user_id=conn_user).aggregate(Sum('save_date')) # today의 시간을 모두 더해서 sum 변수에 담아줌

    values = sum.values() # sam은 딕셔너리 타입이라 values만 따로 가져옴

    for i in values: # 딕셔너리의 values를 for문을 돌려 따로따로 i에 저장함 < 좀어렵
        continue

    context = { # 모든 값을 context에 저장
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'birth_date' : conn_profile.birth_date,
        'timesave' : timesave,
        'plan' : conn_profile.plan,
        'sum' : i,
    }

    return render(request, 'mypage.html', context=context) # context값과 함께 mypage.html을 호출

class ProfileUpdateView(View): # 프로필 수정
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk) 

        conn_user = request.user
        conn_profile = Profile.objects.get(user=conn_user)

        if hasattr(user, 'profile'):  
            profile = user.profile
            profile_form = ProfileUpdateForm(initial={
                'nick': profile.nick,
                'birth_date' : profile.birth_date,
                'plan' : profile.plan,
            })
        else:
            profile_form = ProfileUpdateForm()
            
        context = {
            'profile_form': profile_form,
            'profile': profile,
            'id' : conn_user.username,
            'nick' : conn_profile.nick,
            'birth_date' : profile.birth_date,
            'plan' : profile.plan,
        }

        return render(request, 'profile_update.html', context=context)

    def post(self, request):
        u = User.objects.get(id=request.user.pk)       

        conn_user = request.user
        conn_profile = Profile.objects.get(user=conn_user)

        timesave = Timesave.objects.all()
        sum = Timesave.objects.all().aggregate(Sum('save_date'))
        
        values = sum.values()

        for i in values:
            continue

        if len(request.POST['month']) < 2:
            changeMonth = request.POST['month'].zfill(2)
        else:
            changeMonth=request.POST['month']

        if len(request.POST['day']) < 2:
            changeDay = request.POST['day'].zfill(2)
        else:
            changeDay = request.POST['day']

        changeBirth = request.POST['year']+'-'+changeMonth+'-'+changeDay

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile) 
        else:
            profile_form = ProfileUpdateForm(request.POST, request.FILES)

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            u.password = request.POST['user-password1']
            profile.user = u
            profile.nick = request.POST['profile-nick']
            profile.birth_date = changeBirth
            profile.plan = request.POST['profile-plan']
            profile.save()
            print('정보 수정 성공')
            context = {
                'id' : u.username,
                'nick' : profile.nick,
                'birth_date' : profile.birth_date,
                'timesave' : timesave,
                'plan' : conn_profile.plan,
                'sum' : i,                
            }
            return render(request, 'mypage.html', context=context)
        else :
            print('실패')
        return redirect('mypage', pk=request.user.pk) 
