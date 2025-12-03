from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Member
from .forms import Step1MemberForm, Step2MemberForm
from django.contrib.auth.models import User
# Create your views here.


def registerf(request):

    if request.method == "GET":
        return render(request, 'member_register1.html')
    elif request.method == "POST":
        
        form = Step1MemberForm(request.POST)
        if form.is_valid():
            # 세션에 저장
            request.session['signup_data'] = {
                'm_username': form.cleaned_data['m_username'],
                # 미리 해싱
                'm_password': make_password(form.cleaned_data['m_password1']),
            }
            # 두번째 폼으로
            return redirect('Member:registers')

        return render(request, 'member_register1.html', {'form': form})

    
def registers(request):
    data = request.session.get('signup_data')
    if not data:
        return redirect('Member:registerf')
    
    if request.method == "GET":
        form = Step2MemberForm()
        return render(request, 'member_register2.html', {'form': form})
    
    if request.method == "POST":
        form = Step2MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)

            # Step1 데이터 적용
            member.m_username = data["m_username"]
            member.m_password = data["m_password"]

            member.save()

            del request.session["signup_data"]  # 보안상 제거

            return redirect("Member:login")
        else:
            print(form.errors)

    return render(request, "member_register2.html", {"form": form})

def login(request):
    if request.method == "GET":
        return render(request, 'member_login.html')
    
    elif request.method == "POST":
        m_username = request.POST.get("m_username")
        m_password = request.POST.get("m_password1")
        
        try:
            member = Member.objects.get(m_username=m_username)
        except Member.DoesNotExist:
            # 존재하지 않는 아이디
            return render(request, 'member_login.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})
            
        if check_password(m_password, member.m_password):
            # 로그인 성공
            request.session['member_id'] = member.id
            request.session['member_username'] = member.m_username
            return redirect("Main:main")
        else:
            # 비밀번호 불일치
            return render(request, 'member_login.html', {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})

