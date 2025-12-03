from django.shortcuts import render
from django.conf import settings
from member.models import Member, Individual

def search(request):
    user = request.user

    # 사용자가 로그인하지 않았으면 기본 좌표 사용
    if not user.is_authenticated:
        home = {"x": 14363556.26, "y": 4208115.838}  # 예시 TM 좌표
        work = {"x": 14363800.00, "y": 4208200.00}  # 예시 TM 좌표
        accident_list = []
    else:
        # 사용자 개인 산재 데이터
        user_accidents = Individual.objects.filter(member=user)

        # 드롭다운용 사고지역 리스트 준비 (TM 좌표 포함)
        accident_list = [
            {
                "nickname": acc.nickname,
                "x": acc.x,  # TM x 좌표
                "y": acc.y,  # TM y 좌표
                "address": acc.address
            }
            for acc in user_accidents
            if acc.x and acc.y
        ]

        # 사용자 집/근무지 좌표 (TM 좌표)
        try:
            member = Member.objects.get(id=user.id)
            home = {"x": member.m_address_x, "y": member.m_address_y}
            work = {"x": member.m_jaddress_x, "y": member.m_jaddress_y}
        except Member.DoesNotExist:
            home = {"x": 14363556.26, "y": 4208115.838}
            work = {"x": 14363800.00, "y": 4208200.00}

    return render(request, "search.html", {
        "KAKAO_KEY": settings.KAKAO_KEY,
        "accident_list": accident_list,
        "home": home,
        "work": work
    })
