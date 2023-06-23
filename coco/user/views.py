from django.contrib import auth
from django.contrib.auth import login, logout
from .models import Profile, CustomUser
from .forms import CustomUserSignupForm, CustomUserSigninForm
from django.shortcuts import render, redirect

def signup(request):
    form = CustomUserSignupForm()
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'newSignup.html', {"form":form})
def signin(request):
    form = CustomUserSigninForm()
    if request.method == "POST":
        form = CustomUserSigninForm(request,request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    return render(request, "newSignin.html", {"form":form})
    
def signout(request):
    logout(request)
    return redirect('home')

def new_profile(request):
    #로그인 하지 않았다면 프로필 누르더라도 계속 홈으로 이동
    if request.user.is_anonymous:
        return redirect("home")
    #로그인을 했다면 해당 user의 프로필 보기
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'newProfile.html', {"profile":profile})

def create_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.nickname = request.POST.get('nickname')
        print(profile.nickname)
        profile.image = request.FILES.get('image')
        profile.save()
        return redirect("user:new_profile")
    
    return render(request, "newProfile.html", {"profile":profile})