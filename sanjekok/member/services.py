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
    # 1. Get Access Token
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

    # 2. Get User Profile
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
    nickname = profile_json.get("kakao_account", {}).get("profile", {}).get("nickname")
    if not kakao_id:
        return {'status': 'error', 'message': '사용자 ID를 찾을 수 없습니다.'}
    if not nickname:
        nickname = f"사용자_{kakao_id}"

    # 3. Login or Prepare for Registration
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
