from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Member, Individual, Member_industry
from .forms import Step1MemberForm, Step2MemberForm
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

        return render(request, 'member/member_register1.html', {'form': form})

# 회원가입 2단계    
def registers(request):
    data = request.session.get('signup_data')

    if not data:
        messages.error(request, "첫 번째 회원가입 단계가 만료되었습니다. 다시 진행해주세요.")
        return redirect('Member:registerf')

    if request.method == "GET":
        form = Step2MemberForm()
        return render(request, 'member/member_register2.html', {'form': form})
    
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
        return render(request, "member/member_register2.html", {"form": form})
    
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
    return render(request, 'member/member_complete.html')

# 마이페이지
def mypage(request):
    member_id = request.session.get('member_id')

    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    member = get_object_or_404(Member, member_id=member_id)

    if request.method == "POST":
        password = request.POST.get("m_password1")

        if check_password(password, member.m_password):
            return redirect("Member:mypage_profile")

        return render(request, 'member/mypage_checked.html', {'member': member, 'error': '비밀번호가 일치하지 않습니다.'})

    return render(request, 'member/mypage_checked.html', {'member': member})

# 마이페이지 - 프로필 수정
def mypage_profile(request):

    member_id = request.session.get('member_id')

    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')
    
    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == "GET":
        form = Step2MemberForm(instance=member)
        return render(request, 'member/mypage_profile.html', {'form': form, 'member': member})

    elif request.method == "POST":
        form = Step2MemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 성공적으로 수정되었습니다.")
            return redirect("Member:mypage_profile")

        messages.error(request, "입력값이 잘못되었습니다. 다시 확인해주세요.")
        return render(request, 'member/mypage_profile.html', {'form': form, 'member': member})
    
# 마이페이지 - 산재 관리
def mypage_individual_list(request):
    member_id = request.session.get('member_id')

    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    member = get_object_or_404(Member, member_id=member_id)
    member_industries = member.industries.all()
    individuals = Individual.objects.filter(member_industry__in=member_industries)

    return render(request, 'member/mypage_individual_list.html', {'member': member, 'individuals': individuals})

# 마이페이지 - 산재 추가
def mypage_individual_add(request):
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    member = get_object_or_404(Member, member_id=member_id)

    if request.method == "GET":
        return render(request, 'member/mypage_individual_add.html', {
            'member': member,
        })

    elif request.method == "POST":
        i_title = request.POST.get("i_title")
        i_address = request.POST.get("i_address")
        i_accident_date = request.POST.get("i_accident_date")
        i_injury = request.POST.get("i_injury")
        i_disease_type = request.POST.get("i_disease_type")
        i_industry_type1 = request.POST.get("i_industry_type1")
        i_industry_type2 = request.POST.get("i_industry_type2")

        if not i_industry_type1 or not i_industry_type2:
            return HttpResponseBadRequest("업종을 선택해주세요.")

        member_industry, created = Member_industry.objects.get_or_create(
            member=member,
            i_industry_type1=i_industry_type1,
            i_industry_type2=i_industry_type2
        )
        
        # i_accident_date가 빈 문자열인 경우 None으로 변환
        if not i_accident_date:
            i_accident_date = None

        Individual.objects.create(
            member_industry=member_industry,
            i_title=i_title,
            i_address=i_address,
            i_accident_date=i_accident_date,
            i_injury=i_injury,
            i_disease_type=i_disease_type
        )

        messages.success(request, "산재 정보가 성공적으로 추가되었습니다.")
        return redirect('Member:mypage_individual_list')


# 마이페이지 - 산재 삭제
def mypage_individual_delete(request, individual_id):
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    individual = get_object_or_404(Individual, accident_id=individual_id)
    
    if individual.member_industry.member.member_id != member_id:
        messages.error(request, "삭제할 권한이 없습니다.")
        return redirect('Member:mypage_individual_list')

    if request.method == "POST":
        individual.delete()
        messages.success(request, "산재 정보가 삭제되었습니다.")
    
    return redirect('Member:mypage_individual_list')


# 마이페이지 - 산재 다중 삭제
def mypage_individual_bulk_delete(request):
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_ids')
        if not selected_ids:
            messages.warning(request, "삭제할 항목을 선택해주세요.")
            return redirect('Member:mypage_individual_list')

        # Ensure the user only deletes their own records
        individuals_to_delete = Individual.objects.filter(
            accident_id__in=selected_ids,
            member_industry__member__member_id=member_id
        )
        
        count = individuals_to_delete.count()
        if count > 0:
            individuals_to_delete.delete()
            messages.success(request, f"{count}개의 산재 정보가 삭제되었습니다.")
        else:
            messages.error(request, "삭제할 항목이 없거나 권한이 없습니다.")

    return redirect('Member:mypage_individual_list')



# 로그아웃
def logout(request):
    member_id = request.session.get('member_id')
    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    request.session.flush()
    messages.success(request, "성공적으로 로그아웃되었습니다.", extra_tags='logout-alert')
    return redirect("Main:main")

# 마이페이지 - 회원 탈퇴
def mypage_withdrawal(request):
    member_id = request.session.get('member_id')

    if not member_id:
        messages.error(request, "로그인이 필요합니다.")
        return redirect('Member:login')

    member = get_object_or_404(Member, member_id=member_id)
    
    if request.method == "POST":
        member.m_status = 99
        member.save()
        
        request.session.flush()
        messages.success(request, "회원 탈퇴가 완료되었습니다.", extra_tags='withdrawal-alert')
        return redirect("Main:main")

    return render(request, 'member/mypage_withdrawal.html', {'member': member})

