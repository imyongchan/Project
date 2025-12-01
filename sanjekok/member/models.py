from django.db import models

class Member(models.Model):

    STATUS_CHOICES = [
        (0, '관리자'),  
        (1, '멤버'),    
        (99, '탈퇴자'),   
    ]
    m_sex = models.CharField(max_length=6, verbose_name='성')
    m_birth_date = models.DateField(verbose_name='생년월일')
    m_name = models.CharField(max_length=100, verbose_name='이름')
    m_username = models.CharField(unique=True, max_length=100, verbose_name='회원 아이디')
    m_password = models.CharField(max_length=300, verbose_name='회원 비밀번호')
    m_phone = models.CharField(max_length=11, null=True, verbose_name='회원 전화번호')
    m_address = models.CharField(max_length=150, verbose_name='회원 거주지 주소')
    m_jaddress = models.CharField(max_length=150, verbose_name='회원 근무지 주소')
    m_email = models.EmailField(max_length=100, null=True, verbose_name='회원 이메일')
    m_provider = models.CharField(max_length=100, verbose_name='oauth 제공자')
    m_provider_id = models.CharField(max_length=100, verbose_name='oauth 아이디')
    m_address_lat = models.FloatField(verbose_name='거주지 위도')
    m_address_lng = models.FloatField(verbose_name='거주지 경도')
    m_jaddress_lat = models.FloatField(verbose_name='근무지 위도')
    m_jaddress_lng = models.FloatField(verbose_name='근무지 위도')
    m_created_at = models.DateTimeField(auto_now_add=True, verbose_name='회원 가입일')
    m_status = models.IntegerField(choices=STATUS_CHOICES,default=1,verbose_name='회원 상태')
    

    class Meta:
        db_table = 't_member'
        verbose_name = '사용자'
        verbose_name_plural = '사용자(들)'
    
    def __str__(self):
        return f'[{self.id}:{self.m_username}]'
    

class Individual(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='individuals', verbose_name='회원')
    i_accident_date = models.DateField(null=True, verbose_name='재해일자')
    i_injury = models.CharField(max_length=100, null=True, verbose_name='발생형태')
    i_disease_type = models.CharField(max_length=100, null=True, verbose_name='질병')
    i_address = models.CharField(max_length=150, verbose_name='발생주소')
    i_address_lat = models.FloatField(verbose_name='발생지 위도')
    i_address_lng = models.FloatField(verbose_name='발생지 경도')
    i_title = models.CharField(max_length=10, verbose_name='산재제목')
    
    class Meta:
        db_table = 't_individual'
        verbose_name = '개인산재정보'
        verbose_name_plural = '산재정보(들)'

    def __str__(self):
        return f'[{self.id}:{self.i_title}]'

class Member_industry(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='industries', verbose_name='회원')
    i_industry_type1 = models.CharField(max_length=50,verbose_name='업종중분류1')
    i_industry_type2 = models.CharField(max_length=50, verbose_name='업종중분류2')
    
    class Meta:
        db_table = 't_member_industry'
        verbose_name = '회원 업종 테이블'
        verbose_name_plural = '업종(들)'
    

