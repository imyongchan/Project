from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from hospital.models import Hospital
from member.models import Member
from .models import Review


@require_POST
def review_create(request):
    """
    리뷰 작성 (AJAX용)
    요청 데이터:
      - hospital_id : 병원 PK
      - rating      : 1~5 정수
      - contents    : 리뷰 내용
    세션:
      - member_id   : 로그인한 회원 아이디 (세션에 저장돼 있다고 가정)
    """
    member_id = request.session.get("member_id")
    if not member_id:
        return JsonResponse({"error": "로그인이 필요합니다."}, status=401)

    hospital_id = request.POST.get("hospital_id")
    contents = (request.POST.get("contents") or "").strip()
    rating_str = request.POST.get("rating")

    # 유효성 검사
    if not hospital_id or not contents or not rating_str:
        return HttpResponseBadRequest("필수 값이 누락되었습니다.")

    try:
        rating = int(rating_str)
    except ValueError:
        return HttpResponseBadRequest("평점이 올바르지 않습니다.")

    if rating < 1 or rating > 5:
        return HttpResponseBadRequest("평점은 1~5 사이여야 합니다.")

    hospital = get_object_or_404(Hospital, pk=hospital_id)
    member = get_object_or_404(Member, member_id=member_id)

    review = Review.objects.create(
        hospital=hospital,
        member=member,
        r_contents=contents,
        r_rating=rating,
    )

    return JsonResponse(
        {
            "id": review.id,
            "writer": member.member_id,  # 필요하면 닉네임 필드로 교체
            "contents": review.r_contents,
            "rating": review.r_rating,
            "created_at": review.r_created_at.strftime("%Y-%m-%d"),
        }
    )


@require_GET
def review_list(request, hospital_id: int):
    """
    특정 병원에 대한 리뷰 목록 조회
    GET /reviews/list/<hospital_id>/
    """
    hospital = get_object_or_404(Hospital, pk=hospital_id)

    qs = (
        Review.objects.filter(hospital=hospital)
        .select_related("member")
        .order_by("-r_created_at")
    )

    data = []
    for r in qs:
        data.append(
            {
                "id": r.id,
                "writer": r.member.member_id,  # 필요시 다른 이름 필드 사용
                "contents": r.r_contents,
                "rating": r.r_rating,
                "created_at": r.r_created_at.strftime("%Y-%m-%d"),
            }
        )

    return JsonResponse({"reviews": data})
