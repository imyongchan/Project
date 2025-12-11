from .models import Member, Individual, Member_industry
import requests
from django.conf import settings

def create_individual_accident(member: Member, accident_data: dict):
    """
    산재 정보를 생성합니다.

    Args:
        member (Member): 현재 로그인된 사용자 Member 객체
        accident_data (dict): 산재 정보 데이터
            - i_title (str)
            - i_address (str)
            - i_accident_date (str or None)
            - i_injury (str)
            - i_disease_type (str)
            - i_industry_type1 (str)
            - i_industry_type2 (str)
    """
    member_industry, _ = Member_industry.objects.get_or_create(
        member=member,
        i_industry_type1=accident_data['i_industry_type1'],
        i_industry_type2=accident_data['i_industry_type2']
    )
    
    # i_accident_date가 빈 문자열인 경우 None으로 변환
    i_accident_date = accident_data.get('i_accident_date')
    if not i_accident_date:
        i_accident_date = None

    Individual.objects.create(
        member_industry=member_industry,
        i_title=accident_data['i_title'],
        i_address=accident_data['i_address'],
        i_accident_date=i_accident_date,
        i_injury=accident_data['i_injury'],
        i_disease_type=accident_data['i_disease_type']
    )

def delete_individual_accidents(member_id: int, accident_ids: list) -> int:
    """
    사용자 소유의 여러 산재 정보를 삭제합니다.

    Args:
        member_id (int): 현재 로그인된 사용자의 ID
        accident_ids (list): 삭제할 산재 정보 ID 목록

    Returns:
        int: 삭제된 항목의 수
    """
    individuals_to_delete = Individual.objects.filter(
        accident_id__in=accident_ids,
        member_industry__member__member_id=member_id
    )
    count, _ = individuals_to_delete.delete()
    return count

def handle_kakao_login(code):
    """
    카카오 인증 코드를 사용하여 로그인 또는 회원가입을 처리합니다.

    Args:
        code (str): 카카오로부터 받은 인증 코드

    Returns:
        dict: 처리 결과
            - status ('error'|'login'|'register'): 처리 상태
            - message (str, optional): 오류 메시지
            - user (Member, optional): 로그인 성공 시 사용자 객체
            - signup_data (dict, optional): 회원가입 필요 시 사용자 정보
    """
    # 엑세스 토큰 받기
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "code": code,
    }
    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()

    if token_response.status_code != 200 or token_json.get("error"):
        error_message = token_json.get("error_description", "카카오 인증 실패")
        return {'status': 'error', 'message': error_message}
    
    access_token = token_json.get("access_token")
    if not access_token:
        return {'status': 'error', 'message': '액세스 토큰을 받아올 수 없습니다.'}

    # 2. 사용자 정보 받기
    profile_url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        profile_response = requests.get(profile_url, headers=headers)
        profile_response.raise_for_status()
        profile_json = profile_response.json()
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e)}

    if profile_json.get("code"):
        return {'status': 'error', 'message': profile_json.get('msg')}

    kakao_id = profile_json.get("id")
    kakao_account = profile_json.get("kakao_account") or {}
    profile = kakao_account.get("profile") or {}
    nickname = profile.get("nickname")

    if not kakao_id:
        return {'status': 'error', 'message': '사용자 ID를 찾을 수 없습니다.'}

    if not nickname:
        nickname = f"사용자_{kakao_id}"

    # 3. 기존 사용자 확인 및 처리
    username = f"kakao_{kakao_id}"
    try:
        user = Member.objects.get(m_username=username)
        return {'status': 'login', 'user': user}
    except Member.DoesNotExist:
        signup_data = {
            'm_username': username,
            'm_name': nickname,
            'm_provider': 'kakao',
            'm_provider_id': kakao_id,
        }
        return {'status': 'register', 'signup_data': signup_data}
    

# 네이버 로그인 처리 함수
def handle_naver_login(code, state):
    """
    네이버 인증 코드를 사용하여 로그인 또는 회원가입을 처리합니다.

    Returns:
        dict: {
            status: "error" | "login" | "register",
            message: str,
            user: Member,
            signup_data: dict
        }
    """

    # 1) Access Token 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": settings.NAVER_CLIENT_ID,
        "client_secret": settings.NAVER_CLIENT_SECRET,
        "code": code,
        "state": state,
    }

    token_res = requests.get(token_url, params=token_params).json()
    access_token = token_res.get("access_token")

    if not access_token:
        return {
            "status": "error",
            "message": "액세스 토큰 발급 실패"
        }

    # 2) 유저 정보 요청
    profile_url = "https://openapi.naver.com/v1/nid/me"
    headers = {"Authorization": f"Bearer {access_token}"}

    profile_res = requests.get(profile_url, headers=headers).json()

    if profile_res.get("resultcode") != "00":
        return {
            "status": "error",
            "message": profile_res.get("message", "네이버 프로필 조회 실패")
        }

    profile = profile_res["response"]
    naver_id = profile["id"]
    name = (profile.get("name") or "").strip()

    username = f"naver_{naver_id}"

    # 3) 기존 회원인지 체크
    try:
        user = Member.objects.get(m_username=username)
        return {
            "status": "login",
            "user": user
        }
    except Member.DoesNotExist:
        pass

    # 4) 회원가입 필요
    signup_data = {
        "m_username": username,
        "m_name": name,
        "m_provider": "naver",
        "m_provider_id": naver_id,
    }

    return {
        "status": "register",
        "signup_data": signup_data
    }
    


