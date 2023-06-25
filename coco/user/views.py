from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from .models import Profile, CustomUser
from django.shortcuts import render, redirect
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import os
def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        age = request.POST.get('age')
        password_confirm = request.POST.get('password_confirm')
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            return render(request, 'signup.html')
        if password == password_confirm:
            # 사용자 생성
            user = CustomUser.objects.create_user(
                email=email, password=password, username=username, age=age)
            login(request, user)
            return redirect('new_profile')
    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 사용자 인증
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # 인증 성공 시 로그인 처리
            login(request, user)
            return redirect('user:new_profile')
        else:
            # 인증 실패 시 에러 메시지 출력
            error_message = "Invalid email or password."
            return render(request, 'signin.html', {'error_message': error_message})
    
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('home')


def new_profile(request):
    if request.user.is_anonymous:
        return redirect("user:signin")
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'newProfile.html', {"profile": profile})


def create_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.nickname = request.POST.get('nickname')
        if request.POST.get('remove_image') == 'on':
            delete_image(profile)   
        else:
            profile.image = request.FILES.get('image')        
        profile.save()
        return redirect("user:new_profile")
    return render(request, "newProfile.html", {"profile": profile})


def delete_image(profile):
    # 이미지 파일 삭제
    if profile.image:
        # 이미지 파일의 절대 경로를 가져옴
        image_path = profile.image.path
        # 파일이 존재하면 삭제
        if os.path.exists(image_path):
            os.remove(image_path)

    # DB에서 이미지 정보 제거
    profile.image = None
    profile.save()