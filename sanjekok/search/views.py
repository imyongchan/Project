from django.shortcuts import render
from django.conf import settings
from member.models import Member, Individual  # member 앱 모델 import

def search(request):
    user = request.user

    # 사용자의 개인 산재 데이터 가져오기
    user_accidents = Individual.objects.filter(member=user)

    # 사용자 집, 근무지 좌표
    try:
        member = Member.objects.get(id=user.id)
        home = {"lat": member.m_address_lat, "lng": member.m_address_lng}
        work = {"lat": member.m_jaddress_lat, "lng": member.m_jaddress_lng}
    except Member.DoesNotExist:
        home = {"lat": 37.5700, "lng": 126.9768}  # 기본값
        work = {"lat": 37.5665, "lng": 126.9780}  # 기본값

    return render(request, "search/search.html", {
        "KAKAO_KEY": settings.KAKAO_KEY,
        "user_accidents": user_accidents,
        "home": home,
        "work": work
    })
