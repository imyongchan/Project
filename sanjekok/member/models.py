from django.db import models
from django.core.validators import RegexValidator

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)

    STATUS_CHOICES = [
        (0, '관리자'),
        (1, '멤버'),
        (99, '탈퇴자'),
    ]

    SEX_CHOICES = [
        ('남성', '남성'),
        ('여성', '여성'),
    ]

    m_sex = models.CharField(max_length=6, choices=SEX_CHOICES, verbose_name='성')
    m_birth_date = models.DateField(verbose_name='생년월일')
    
    # 한글, 영어, 숫자만 허용, 1~20자
    name_validator = RegexValidator(
        regex=r'^(?=.*[가-힣a-zA-Z0-9])[가-힣a-zA-Z0-9_](?:[가-힣a-zA-Z0-9_ ]{0,18}[가-힣a-zA-Z0-9_])?$',
        message='이름은 한글, 영어, 숫자, _, 공백만 입력 가능하며 1~20글자까지 가능합니다.'
    )

    m_name = models.CharField(
        max_length=20,
        validators=[name_validator],
        verbose_name='이름'
    )

    m_username = models.CharField(unique=True, max_length=100, verbose_name='회원 아이디')
    m_password = models.CharField(max_length=300, verbose_name='회원 비밀번호')
    m_phone = models.CharField(max_length=11, null=True, verbose_name='회원 전화번호')
    m_address = models.CharField(max_length=150, verbose_name='회원 거주지 주소')
    m_jaddress = models.CharField(max_length=150, verbose_name='회원 근무지 주소')
    m_email = models.EmailField(max_length=100, null=True, verbose_name='회원 이메일')
    m_provider = models.CharField(max_length=100, null=True, verbose_name='oauth 제공자', default='local')
    m_provider_id = models.CharField(max_length=100, null=True, verbose_name='oauth 아이디')
    m_created_at = models.DateTimeField(auto_now_add=True, verbose_name='회원 가입일')
    m_status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='회원 상태')

    class Meta:
        db_table = 't_member'
        verbose_name = '사용자'
        verbose_name_plural = '사용자(들)'

    def __str__(self):
        return f'[{self.member_id}:{self.m_username}]'
    


class Member_industry(models.Model):
    member_industry = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='industries', verbose_name='회원')
    i_industry_type1 = models.CharField(max_length=50, verbose_name='업종중분류1')
    i_industry_type2 = models.CharField(max_length=50, verbose_name='업종중분류2')

    class Meta:
        db_table = 't_member_industry'
        verbose_name = '회원 업종 테이블'
        verbose_name_plural = '업종(들)'



class Individual(models.Model):

    
    title_validator = RegexValidator(
        regex=r'^[가-힣a-zA-Z0-9]+$',
        message='산재제목은 한글, 영어, 숫자만 입력 가능합니다.'
    )


    accident_id = models.AutoField(primary_key=True)
    member_industry = models.ForeignKey(Member_industry, on_delete=models.CASCADE, related_name='individuals', verbose_name='회원 업종')
    i_accident_date = models.DateField(null=True, verbose_name='재해일자')
    i_injury = models.CharField(max_length=100, null=True, verbose_name='발생형태')
    i_disease_type = models.CharField(max_length=100, null=True, verbose_name='질병')
    i_address = models.CharField(max_length=150, verbose_name='발생주소')
    i_lat = models.FloatField(null=True, blank=True, verbose_name="사고위치 위도")
    i_lng = models.FloatField(null=True, blank=True, verbose_name="사고위치 경도")
    i_title = models.CharField(
        max_length=10,
        validators=[title_validator],
        verbose_name='산재제목'
    )

    class Meta:
        db_table = 't_individual'
        verbose_name = '개인산재정보'
        verbose_name_plural = '산재정보(들)'

    def __str__(self):
        return f'[{self.accident_id}:{self.i_title}]'
