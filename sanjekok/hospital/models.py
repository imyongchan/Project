from django.db import models

class Hospital(models.Model):
    h_hospital_name = models.CharField(max_length=100,verbose_name='의료기관명')
    h_address = models.CharField(max_length=150,verbose_name='소재지')
    h_phone_number = models.CharField(max_length=11,verbose_name='전화번호')
    h_hospital_type = models.CharField(max_length=100,verbose_name='종별')
    h_rc = models.CharField(max_length=100,null=True,verbose_name='부가기능(재활인증, 진폐요양)')
    h_rc_info = models.CharField(max_length=100,null=True,verbose_name='재활인증(만료일)')
    h_tr = models.CharField(max_length=100,null=True,verbose_name='진료제한(기간)')
    h_ei = models.CharField(max_length=100,null=True,verbose_name='의료기관평가(평가연도)')

    class Meta:
        db_table = 't_hospital'
        verbose_name = '산재지정병원'
        verbose_name_plural = '산재지정병원 목록'

    def __str__(self):
        return self.h_hospital_name
