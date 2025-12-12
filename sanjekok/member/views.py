from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Member, Individual, Member_industry
from .forms import Step1MemberForm, Step2MemberForm
from .decorators import login_required, mypage_auth_required
from . import services
from django.conf import settings
import urllib.parse
# Create your views here.

# 약관 동의
def agree(request):

    if request.method == "GET":
        return render(request, 'member/member_agree.html')
    
    if request.method == "POST":
        agree_term = request.POST.get("agree_term")
        agree_privacy = request.POST.get("agree_priv")

        if agree_term == "1" and agree_privacy == "1":
            return redirect('Member:registerf')
        else:
            messages.error(request, "약관 및 개인정보처리방침에 동의하셔야 회원가입이 가능합니다.")
            return render(request, 'member/member_agree.html')

# 회원가입 1단계
def registerf(request):

    if request.method == "GET":
        return render(request, 'member/member_register1.html')
    
    elif request.method == "POST":
        form = Step1MemberForm(request.POST)
        if form.is_valid():
            # 세션 저장
            request.session['signup_data'] = {
                'm_username': form.cleaned_data['m_username'],
                'm_password': make_password(form.cleaned_data['m_password1']),
            }
            return redirect('Member:registers')

        first_error_field = next(iter(form.errors)) if form.errors else None
        context = {
            "form": form,
            "first_error_field": first_error_field,
        }
        return render(request, 'member/member_register1.html', context)

# 회원가입 2단계    
def registers(request):
    signup_data = request.session.get('signup_data')
    social_signup_data = request.session.get('social_signup_data')

    if not signup_data and not social_signup_data:
        messages.error(request, "회원가입 정보가 만료되었습니다. 다시 진행해주세요.")
        return redirect('Member:registerf')

    if request.method == "GET":
        initial_data = {}
        if social_signup_data:
            initial_data['m_name'] = social_signup_data.get('m_name')
        form = Step2MemberForm(initial=initial_data)
        return render(request, 'member/member_register2.html', {'form': form})
    
    elif request.method == "POST":
        form = Step2MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            
            if social_signup_data:
                member.m_username = social_signup_data['m_username']
                member.m_provider = social_signup_data['m_provider']
                member.m_provider_id = social_signup_data.get('m_provider_id')
                member.m_password = make_password(None)
                if 'social_signup_data' in request.session:
                    del request.session['social_signup_data']
            elif signup_data:
                member.m_username = signup_data['m_username']
                member.m_password = signup_data['m_password']
                if 'signup_data' in request.session:
                    del request.session['signup_data']
            
            member.save()

            messages.success(request, "회원가입이 완료되었습니다.")
            
            # 세션에 사용자 정보 저장
            request.session['member_id'] = int(member.member_id)
            request.session['member_username'] = member.m_username
            request.session['member_name'] = member.m_name  # 사용자 이름 추가
            request.session['member_provider'] = member.m_provider

            if member.m_provider != 'local':
                # Social login user
                messages.success(request, f"{member.m_name}님 환영합니다!")
                return redirect("Main:main")
            else:
                # Regular user
                messages.success(request, f"{member.m_name}님, 회원가입을 환영합니다!")
                return redirect('Main:main') # 'Member:complete' 대신 'Main:main'으로 변경


        first_error_field = next(iter(form.errors)) if form.errors else None
        context = {
            "form": form,
            "first_error_field": first_error_field,
        }
        messages.error(request, "입력값이 올바르지 않습니다. 다시 입력해주세요.")
        return render(request, "member/member_register2.html", context)
    
# 로그인
def login(request):
    if request.method == "GET":
        return render(request, "member/member_login.html")

    elif request.method == "POST":
        m_username = request.POST.get("m_username")
        m_password = request.POST.get("m_password1")

        member = Member.objects.filter(m_username=m_username).first()

        if not member or not check_password(m_password, member.m_password) or member.m_status == 99:
            messages.error(request, "아이디 또는 비밀번호가 일치하지 않습니다.")
            return render(request, "member/member_login.html")

        request.session['member_id'] = int(member.member_id)
        request.session['member_name'] = member.m_name
        request.session['member_provider'] = member.m_provider

        messages.success(request, f"{member.m_name}님 환영합니다!")
        return redirect("Main:main")
    
def kakao_login(request):
    kakao_rest_api_key = settings.KAKAO_REST_API_KEY
    
    redirect_uri = settings.KAKAO_REDIRECT_URI
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={kakao_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


# 2) 카카오에서 인증 후 콜백 처리
def kakao_callback(request):
    code = request.GET.get("code")
    if not code:
        messages.error(request, "카카오 로그인에 실패했습니다. (인증 코드 없음)")
        return redirect("Member:login")

    result = services.handle_kakao_login(code)

    if result['status'] == 'error':
        messages.error(request, f"카카오 로그인 실패: {result['message']}")
        return redirect("Member:login")
    
    elif result['status'] == 'login':
        user = result['user']
        request.session['member_id'] = int(user.member_id)
        request.session['member_name'] = user.m_name
        request.session['member_provider'] = user.m_provider
        messages.success(request, f"{user.m_name}님 환영합니다!")
        return redirect("Main:main")

    elif result['status'] == 'register':
        request.session['social_signup_data'] = result['signup_data']
        return redirect('Member:registers')

# 네이버 로그인
def naver_login(request):
    base_url = "https://nid.naver.com/oauth2.0/authorize"
    params = {
        "response_type": "code",
        "client_id": settings.NAVER_CLIENT_ID,
        "redirect_uri": settings.NAVER_REDIRECT_URI,
        "state": "RANDOM_STATE_STRING",
    }
    return redirect(f"{base_url}?{urllib.parse.urlencode(params)}")

# 네이버 로그인 콜백
def naver_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    result = services.handle_naver_login(code, state)

    if result['status'] == 'error':
        messages.error(request, f"네이버 로그인 실패: {result['message']}")
        return redirect("Member:login")

    elif result['status'] == 'login':
        user = result['user']
        request.session['member_id'] = int(user.member_id)
        request.session['member_name'] = user.m_name
        request.session['member_provider'] = user.m_provider
        messages.success(request, f"{user.m_name}님 환영합니다!")
        return redirect("Main:main")

    elif result['status'] == 'register':
        request.session['social_signup_data'] = result['signup_data']
        return redirect("Member:registers")

# 구글 로그인
def google_login(request):
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    return redirect(f"{base_url}?{urllib.parse.urlencode(params)}")


def google_callback(request):
    code = request.GET.get("code")

    if not code:
        messages.error(request, "구글 로그인에 실패했습니다. (인증 코드 없음)")
        return redirect("Member:login")

    result = services.handle_google_login(code)

    if result["status"] == "error":
        messages.error(request, f"구글 로그인 실패: {result['message']}")
        return redirect("Member:login")

    elif result["status"] == "login":
        user = result["user"]
        request.session["member_id"] = int(user.member_id)
        request.session["member_name"] = user.m_name
        request.session["member_provider"] = user.m_provider
        messages.success(request, f"{user.m_name}님 환영합니다!")
        return redirect("Main:main")

    elif result["status"] == "register":
        request.session["social_signup_data"] = result["signup_data"]
        return redirect("Member:registers")

# 아이디 중복 확인
def check_username(request):
    username = request.GET.get('username')
    data = {
        'is_taken': Member.objects.filter(m_username=username).exists()
    }
    return JsonResponse(data)


# 마이페이지 - 비밀번호 확인
@login_required
def mypage_check(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)

    # 소셜 로그인 사용자는 이 페이지에 접근할 이유가 없음
    if member.m_provider != 'local':
        request.session['mypage_authorized'] = True
        return redirect("Member:mypage_profile")

    if request.method == "POST":
        password = request.POST.get("m_password1")

        if check_password(password, member.m_password):
            request.session['mypage_authorized'] = True
            # 원래 가려던 URL이 있으면 거기로 리디렉션
            next_url = request.session.pop('next_url', None)
            if next_url:
                return redirect(next_url)
            return redirect("Member:mypage_profile")

        return render(request, 'member/mypage_checked.html', {'member': member, 'error': '비밀번호가 일치하지 않습니다.'})

    return render(request, 'member/mypage_checked.html', {'member': member})

# 마이페이지 - 프로필
@mypage_auth_required
def mypage_profile(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)
    return render(request, 'member/mypage_profile.html', {'member': member})



# 마이페이지 - 프로필 수정
@mypage_auth_required
def mypage_profile_modify(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == "GET":
        form = Step2MemberForm(instance=member)
        return render(request, 'member/mypage_profile_modify.html', {'form': form, 'member': member})

    elif request.method == "POST":
        form = Step2MemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 수정되었습니다.")
            return redirect("Member:mypage_profile")

        first_error_field = next(iter(form.errors)) if form.errors else None
        context = {
            'form': form,
            'member': member,
            'first_error_field': first_error_field
        }
        messages.error(request, "입력값이 잘못되었습니다. 다시 확인해주세요.")
        return render(request, 'member/mypage_profile_modify.html', context)
    
# 마이페이지 - 산재 관리
@mypage_auth_required
def mypage_individual_list(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)
    member_industries = member.industries.all()
    individuals = Individual.objects.filter(member_industry__in=member_industries)

    return render(request, 'member/mypage_individual_list.html', {'member': member, 'individuals': individuals})

# 마이페이지 - 산재 추가
@mypage_auth_required
def mypage_individual_add(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)

    if request.method == "GET":
        return render(request, 'member/mypage_individual_add.html', {
            'member': member,
        })

    elif request.method == "POST":
        i_industry_type1 = request.POST.get("i_industry_type1")
        i_industry_type2 = request.POST.get("i_industry_type2")

        if not i_industry_type1 or not i_industry_type2:
            return HttpResponseBadRequest("업종을 선택해주세요.")

        accident_data = {
            'i_title': request.POST.get("i_title"),
            'i_address': request.POST.get("i_address"),
            'i_accident_date': request.POST.get("i_accident_date"),
            'i_injury': request.POST.get("i_injury"),
            'i_disease_type': request.POST.get("i_disease_type"),
            'i_industry_type1': i_industry_type1,
            'i_industry_type2': i_industry_type2,
        }
        
        services.create_individual_accident(member, accident_data)

        messages.success(request, "산재 정보가 성공적으로 추가되었습니다.")
        return redirect('Member:mypage_individual_list')


# 마이페이지 - 산재 삭제
@mypage_auth_required
def mypage_individual_delete(request, individual_id):
    member_id = request.session.get('member_id')
    individual = get_object_or_404(Individual, accident_id=individual_id)
    
    try:
        # 해당 산재 정보가 현재 로그인한 사용자의 것인지 확인
        Member_industry.objects.get(member=member_id, industries__accident_id=individual_id)
    except Member_industry.DoesNotExist:
        messages.error(request, "삭제할 권한이 없습니다.")
        return redirect('Member:mypage_individual_list')

    if request.method == "POST":
        individual.delete()
        messages.success(request, "산재 정보가 삭제되었습니다.")
    
    return redirect('Member:mypage_individual_list')


# 마이페이지 - 산재 다중 삭제
@mypage_auth_required
def mypage_individual_bulk_delete(request):
    member_id = request.session.get('member_id')

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_ids')
        if not selected_ids:
            messages.warning(request, "삭제할 항목을 선택해주세요.")
            return redirect('Member:mypage_individual_list')

        count = services.delete_individual_accidents(member_id, selected_ids)
        
        if count > 0:
            messages.success(request, f"{count}개의 산재 정보가 삭제되었습니다.")
        else:
            messages.error(request, "삭제할 항목이 없거나 권한이 없습니다.")

    return redirect('Member:mypage_individual_list')



# 로그아웃
@login_required
def logout(request):
    member_id = request.session.get('member_id')
    provider = 'local' 

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            provider = member.m_provider
        except Member.DoesNotExist:
            pass 

    # 세션 데이터를 삭제하여 우리 앱에서 로그아웃
    request.session.flush()
    messages.success(request, "성공적으로 로그아웃되었습니다.", extra_tags='logout-alert')

    # 소셜 사용자인 경우, 해당 소셜 서비스에서 로그아웃 처리
    if provider == 'kakao':
        kakao_rest_api_key = settings.KAKAO_REST_API_KEY
        logout_redirect_uri = settings.KAKAO_LOGOUT_REDIRECT_URI
        
        kakao_logout_url = (
            f"https://kauth.kakao.com/oauth/logout"
            f"?client_id={kakao_rest_api_key}"
            f"&logout_redirect_uri={logout_redirect_uri}"
        )
        return redirect(kakao_logout_url)
    
    # --- 네이버 로그아웃 ---
    if provider == 'naver':
        # 네이버는 서버 API 로그아웃 없음 → 로그인 페이지 세션만 끊음
        return redirect("Main:main")

    # 로컬 사용자는 메인 페이지로 리디렉션
    return redirect("Main:main")

# 마이페이지 - 비밀번호 변경
@mypage_auth_required
def mypage_password_change(request):
    if request.session.get('member_provider') != 'local':
        messages.error(request, "소셜 로그인 사용자는 비밀번호를 변경할 수 없습니다.")
        return redirect("Main:main")
        
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)

    if request.method == "GET":
        return render(request, 'member/mypage_password_change.html', {'member': member})

    elif request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not check_password(current_password, member.m_password):
            messages.error(request, "현재 비밀번호가 일치하지 않습니다.")
            return render(request, 'member/mypage_password_change.html', {'member': member})

        if new_password1 != new_password2:
            messages.error(request, "새 비밀번호가 일치하지 않습니다.")
            return render(request, 'member/mypage_password_change.html', {'member': member})

        member.m_password = make_password(new_password1)
        member.save()

        messages.success(request, "비밀번호가 성공적으로 변경되었습니다.")
        return redirect("Member:mypage_profile")
    
    


# 마이페이지 - 회원 탈퇴
@mypage_auth_required
def mypage_withdrawal(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == "POST":
        member.m_status = 99
        member.save()
        
        request.session.flush()
        messages.success(request, "회원 탈퇴가 완료되었습니다.", extra_tags='withdrawal-alert')
        return redirect("Main:main")

    return render(request, 'member/mypage_withdrawal.html', {'member': member})
