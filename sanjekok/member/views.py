from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse
from .models import Member
from .forms import Step1MemberForm, Step2MemberForm
# Create your views here.

# 회원가입 1단계
def registerf(request):

    if request.method == "GET":
        return render(request, 'member_register1.html')
    
    elif request.method == "POST":
        form = Step1MemberForm(request.POST)
        if form.is_valid():
            # 세션 저장
            request.session['signup_data'] = {
                'm_username': form.cleaned_data['m_username'],
                'm_password': make_password(form.cleaned_data['m_password1']),
            }
            return redirect('Member:registers')

        return render(request, 'member_register1.html', {'form': form})

# 회원가입 2단계    
def registers(request):
    data = request.session.get('signup_data')

    if not data:
        messages.error(request, "첫 번째 회원가입 단계가 만료되었습니다. 다시 진행해주세요.")
        return redirect('Member:registerf')

    if request.method == "GET":
        form = Step2MemberForm()
        return render(request, 'member_register2.html', {'form': form})
    
    elif request.method == "POST":
        form = Step2MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.m_username = data['m_username']
            member.m_password = data['m_password']
            member.save()

            # 보안상 세션 제거
            del request.session["signup_data"]

            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect('Member:complete')

        messages.error(request, "입력값이 올바르지 않습니다. 다시 입력해주세요.")
        return render(request, "member_register2.html", {"form": form})
    
# 로그인
def login(request):
    if request.method == "GET":
        return render(request, "member_login.html")

    elif request.method == "POST":
        m_username = request.POST.get("m_username")
        m_password = request.POST.get("m_password1")

        member = Member.objects.filter(m_username=m_username).first()

        if not member or not check_password(m_password, member.m_password):
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "member_login.html")

        request.session['member_id'] = member.id
        request.session['member_username'] = member.m_username

        messages.success(request, f"{member.m_username}님 환영합니다!")
        return redirect("Main:main")

# 아이디 중복 확인
def check_username(request):
    username = request.GET.get('username')
    data = {
        'is_taken': Member.objects.filter(m_username=username).exists()
    }
    return JsonResponse(data)

def complete(request):
    return render(request, 'member_complete.html')

# 마이페이지
def mypage(request):
    member_id = request.session.get('member_id')

    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        password = request.POST.get("m_password1")

        if check_password(password, member.m_password):
            return redirect("Member:mypage_profile")

        messages.error(request, "비밀번호가 일치하지 않습니다.")
        return render(request, 'mypage_checked.html', {'member': member})

    return render(request, 'mypage_checked.html', {'member': member})

# 마이페이지 - 프로필 수정
def mypage_profile(request):

    member_id = request.session.get('member_id')

    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')
    
    member = get_object_or_404(Member, id=member_id)
    
    if request.method == "GET":
        form = Step2MemberForm(instance=member)
        return render(request, 'mypage_profile.html', {'form': form, 'member': member})

    elif request.method == "POST":
        form = Step2MemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 수정되었습니다.")
            return redirect("Member:mypage_profile")

        messages.error(request, "입력값이 잘못되었습니다. 다시 확인해주세요.")
        return render(request, 'mypage_profile.html', {'form': form, 'member': member})

