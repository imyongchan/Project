from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F

from .crawler.run import crawl_safe
from .models import Safe
from .models import History
from member.models import Member

def is_admin(user):
    """
    관리자 여부 판단
    """
    return user.is_staff or user.is_superuser


# 1) 관리자용: 수동 크롤링 실행
def crawl_safe_view(request):
    """
    /news/crawl/ 로 접근했을 때 크롤링 실행
    """
    try:
        crawl_safe()
        messages.success(request, "크롤링 완료!")
    except Exception as e:
        messages.error(request, f"크롤링 중 오류 발생: {e}")
    return redirect("Safe:safe_list")


# 2) 안전자료 목록 페이지
@login_required
def safe_list(request):

    # ----------------------------------------
    # 최근 조회한 자료
    # ----------------------------------------
    member_id = request.session.get("member_id")

    recent_list = []

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            recent_list = (
                History.objects
                .filter(member=member)
                .select_related("safe")
                .order_by("-h_vdate")[:6]
            )
        except Member.DoesNotExist:
            recent_list = []

    # 기본 목록
    materials = Safe.objects.all()

    # ----------------------------------------
    # 필터 목록 제공 (템플릿 사용용)
    # ----------------------------------------
    type_list = ["전체", "OPS", "동영상", "책자", "교안(PPT)", "기타"]
    language_list = ["전체", "한국어", "외국어"]

    BASE_TYPES = ["OPS", "동영상", "책자", "교안(PPT)"]

    # ----------------------------------------
    #  자료유형 체크박스
    # ----------------------------------------
    selected_types = request.GET.getlist("type")

    if not selected_types:
        selected_types = ["전체"]

    if "전체" not in selected_types:
        filtered_ids = []

        for item in materials:
            t = item.s_type

            if t in selected_types:
                filtered_ids.append(item.id)
                continue

            # 기타 선택 시 BASE_TYPES 에 없는 유형만 포함
            if "기타" in selected_types and t not in BASE_TYPES:
                filtered_ids.append(item.id)
                continue

        materials = materials.filter(id__in=filtered_ids)

    # ----------------------------------------
    #  언어 필터링
    # ----------------------------------------
    selected_language = request.GET.get("lang", "전체")

    if selected_language == "한국어":
        materials = materials.filter(s_language="한국어")
    elif selected_language == "외국어":
        materials = materials.exclude(s_language="한국어")

    # ----------------------------------------
    #  검색
    # ----------------------------------------
    q = request.GET.get("q", "").strip()

    if q:
        materials = materials.filter(s_title__icontains=q)

    # ----------------------------------------
    #  정렬
    # ----------------------------------------
    sort = request.GET.get("sort", "latest")

    if sort == "latest":
        materials = materials.order_by("-s_created_at", "-id")
    elif sort == "oldest":
        materials = materials.order_by("s_created_at", "id")
    elif sort == "views":
        materials = materials.order_by("-s_view_count", "-s_created_at")



    # ----------------------------------------
    #  페이지네이션
    # ----------------------------------------
    WRITE_PAGES = 5
    PER_PAGE = 12

    page = request.GET.get("page", 1)

    paginator = Paginator(materials, PER_PAGE)
    page_obj = paginator.get_page(page)

    start_page = ((page_obj.number - 1) // WRITE_PAGES) * WRITE_PAGES + 1
    end_page = min(start_page + WRITE_PAGES - 1, paginator.num_pages)
    page_range = range(start_page, end_page + 1)
    
    # 현재 GET 파라미터 딕셔너리
    params = request.GET.copy()

    # 페이지 번호는 매번 새로 넣을 것이므로 제거
    if "page" in params:
        params.pop("page")

    # 새 파라미터 문자열 생성
    querystring = params.urlencode()

    context = {
        "list": page_obj,
        "page_obj": page_obj,
        "start_page": start_page,
        "end_page": end_page,
        "page_range": page_range,

        # 최근 조회한 자료 리스트
        "recent_list": recent_list,

        # 필터 유지용
        "selected_types": selected_types,
        "selected_language": selected_language,
        "search_keyword": q,
        "sort" : sort,

        # 템플릿용
        "type_list": type_list,
        "language_list": language_list,

        # 파라미터
        "querystring": querystring,
        
        
    }

    return render(request, "safe/safe_list.html", context)

# 3) 안전자료 상세페이지
def safe_detail(request, pk):
    safe = get_object_or_404(Safe, pk=pk)
    
    # 조회수 증가
    Safe.objects.filter(pk=safe.pk).update(
        s_view_count=F('s_view_count') + 1
    )
    safe.refresh_from_db()

    # -----------------------------
    # 최근 조회 기록 저장 (세션 기반)
    # -----------------------------
    member_id = request.session.get("member_id")

    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)

            History.objects.update_or_create(
                member=member,
                safe=safe
            )

            print("✅ History 저장:", member.m_username, safe.id)

        except Member.DoesNotExist:
            print("❌ Member 없음:", member_id)

    # 연관 콘텐츠
    tags = safe.tags.all()
    related = Safe.objects.filter(tags__in=tags).exclude(id=safe.id).distinct()
    related = related.order_by('-s_view_count', '-s_created_at')[:8]

    return render(request, "safe/safe_detail.html", {
        "safe": safe,
        "related_list": related,
    })
