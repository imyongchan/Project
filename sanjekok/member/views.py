from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Member, Individual, Member_industry
from .forms import Step1MemberForm, Step2MemberForm
from .decorators import login_required
from . import services
from django.conf import settings
import requests
from django.urls import reverse
# Create your views here.

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
            
            request.session['member_id'] = int(member.member_id)
            request.session['member_username'] = member.m_username

            if member.m_provider != 'local':
                # Social login user
                messages.success(request, f"{member.m_name}님 환영합니다!")
                return redirect("Main:main")
            else:
                # Regular user
                return redirect('Member:complete')

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
        request.session['member_username'] = member.m_username

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

    kakao_rest_api_key = settings.KAKAO_REST_API_KEY
    print("--- DEBUG ---")
    print(f"Using KAKAO_REST_API_KEY: {kakao_rest_api_key}")
    print("---------------")
    redirect_uri = settings.KAKAO_REDIRECT_URI

    # --- Access Token 요청 ---
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": kakao_rest_api_key,
        "redirect_uri": redirect_uri,
        "code": code,
    }
    
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()

    if token_response.status_code != 200:
        error_description = token_json.get("error_description", "알 수 없는 오류가 발생했습니다.")
        messages.error(request, f"카카오 로그인 실패: {error_description}")
        return redirect("Member:login")

    if token_json.get("error"):
        messages.error(request, f"카카오 로그인 실패: {token_json.get('error_description')}")
        return redirect("Member:login")

    access_token = token_json.get("access_token")
    if not access_token:
        messages.error(request, "카카오 로그인 실패: 액세스 토큰을 받아올 수 없습니다.")
        return redirect("Member:login")

    # --- 사용자 정보 요청 ---
    profile_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        profile_response = requests.get(profile_url, headers=headers)
        profile_response.raise_for_status()
        profile_json = profile_response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"카카오 로그인 실패: {e}")
        return redirect("Member:login")

    if profile_json.get("code"):
        messages.error(request, f"카카오 로그인 실패: {profile_json.get('msg')}")
        return redirect("Member:login")

    kakao_id = profile_json.get("id")
    if not kakao_id:
        messages.error(request, "카카오 로그인 실패: 사용자 ID를 찾을 수 없습니다.")
        return redirect("Member:login")
        
    nickname = profile_json.get("kakao_account", {}).get("profile", {}).get("nickname")
    if not nickname:
        # 닉네임은 필수 동의 항목이 아닌 경우가 있으므로, 없으면 기본값 설정
        nickname = f"사용자_{kakao_id}"

    try:
        user = Member.objects.get(m_username=f"kakao_{kakao_id}")
        
        request.session['member_id'] = int(user.member_id)
        request.session['member_username'] = user.m_username
        messages.success(request, f"{user.m_name}님 환영합니다!")
        return redirect("Main:main")
    except Member.DoesNotExist:
        
        request.session['social_signup_data'] = {
            'm_username': f"kakao_{kakao_id}",
            'm_name': nickname,
            'm_provider': 'kakao',
            'm_provider_id': kakao_id,
        }
        return redirect('Member:registers')



# 아이디 중복 확인
def check_username(request):
    username = request.GET.get('username')
    data = {
        'is_taken': Member.objects.filter(m_username=username).exists()
    }
    return JsonResponse(data)

def complete(request):
    return render(request, 'member/member_complete.html')

# 마이페이지 - 비밀번호 확인
@login_required
def mypage(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)

    if request.method == "POST":
        password = request.POST.get("m_password1")

        if check_password(password, member.m_password):
            return redirect("Member:mypage_profile")

        return render(request, 'member/mypage_checked.html', {'member': member, 'error': '비밀번호가 일치하지 않습니다.'})

    return render(request, 'member/mypage_checked.html', {'member': member})

# 마이페이지 - 프로필
@login_required
def mypage_profile(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)
    return render(request, 'member/mypage_profile.html', {'member': member})



# 마이페이지 - 프로필 수정
@login_required
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
@login_required
def mypage_individual_list(request):
    member_id = request.session.get('member_id')
    member = get_object_or_404(Member, member_id=member_id)
    member_industries = member.industries.all()
    individuals = Individual.objects.filter(member_industry__in=member_industries)

    return render(request, 'member/mypage_individual_list.html', {'member': member, 'individuals': individuals})

# 마이페이지 - 산재 추가
@login_required
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
@login_required
def mypage_individual_delete(request, individual_id):
    member_id = request.session.get('member_id')
    individual = get_object_or_404(Individual, accident_id=individual_id)
    
    if individual.member_industry.member.member_id != member_id:
        messages.error(request, "삭제할 권한이 없습니다.")
        return redirect('Member:mypage_individual_list')

    if request.method == "POST":
        individual.delete()
        messages.success(request, "산재 정보가 삭제되었습니다.")
    
    return redirect('Member:mypage_individual_list')


# 마이페이지 - 산재 다중 삭제
@login_required
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
    provider = 'local' # Default provider

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            provider = member.m_provider
        except Member.DoesNotExist:
            pass # Member not found, proceed with default logout

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

    # 로컬 사용자는 메인 페이지로 리디렉션
    return redirect("Main:main")

# 마이페이지 - 비밀번호 변경
@login_required
def mypage_password_change(request):
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
@login_required
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

