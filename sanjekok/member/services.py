from .models import Member, Individual, Member_industry

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
