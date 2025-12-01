from django.db import models
from hospital.models import Hospital
from member.models import Member

class Review(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE,related_name='reviews',verbose_name='리뷰가 작성된 병원')
    member = models.ForeignKey(Member,on_delete=models.CASCADE,related_name='reviews',verbose_name='리뷰 작성한 회원')
    r_contents = models.TextField(verbose_name='리뷰내용')
    r_created_at = models.DateTimeField(auto_now_add=True,verbose_name='리뷰작성일')
    r_rating = models.IntegerField(verbose_name='평점')

    class Meta:
        db_table = 't_review'
        verbose_name = '병원 리뷰'
        verbose_name_plural = '병원 리뷰 목록'

    def __str__(self):
        return self.r_contents