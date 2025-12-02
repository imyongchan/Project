from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Member
# Create your views here.


def register(request):

    if request.method == "GET":
        return render(request, 'member_register.html')
    elif request.method == "POST":
        username = request.POST['username']   # name='username' 값을 받아온다
        useremail = request.POST['useremail']
        password = request.POST['password']   # name='password' 값을 받아온다
        re_password = request.POST['re-password']   # name='re-password' 값을 받아온다

        res_data = {}  # response 에 전달할 데이터 준비

        # 빈 문자, 값이 없으면 검증 에러
        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야 합니다.'

        # password 와 re_password 가 다르면 검증 에러
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
        else:

            member = Member(
                username=username,
                useremail=useremail,
                password=make_password(password)  # 암호화 하여 저장.
                )

            member.save()

        return render(request, 'member_register.html', res_data)
