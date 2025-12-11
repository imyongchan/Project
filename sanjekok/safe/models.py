from django.db import models
from member.models import Member

class Tag(models.Model):
    st_tag = models.CharField(unique=True, max_length=100, verbose_name="태그명")

    class Meta:
        db_table = 't_tag'
        verbose_name = '안전자료실 태그'
        verbose_name_plural = '안전자료실 태그(들)'
        
    def __str__(self):
        return self.st_tag

class Safe(models.Model):
    s_title = models.CharField(max_length=150, verbose_name='안전 자료 제목')
    s_image_url = models.URLField(max_length=2000, verbose_name='안전 자료 이미지 url')
    s_type = models.CharField(max_length=30, verbose_name='안전 자료 형태')
    s_contents = models.TextField(null=True, verbose_name='안전 자료 내용')
    s_created_at = models.DateField(null=True, verbose_name='안전 자료 작성일')
    s_view_count = models.IntegerField(verbose_name='조회수', default=0)
    s_link = models.URLField(max_length=2000, verbose_name='안전 상세페이지 링크')
    s_language = models.CharField(max_length=50, null=True) 
    s_publisher = models.CharField(max_length=100, verbose_name='자료 출처명', default='KOSHA')
    
    s_video_url = models.URLField(max_length=2000, null=True, verbose_name='안전 자료 동영상 url')

    tags = models.ManyToManyField(Tag, through='SafeTag', related_name='materials', verbose_name='태그')

    class Meta:
        db_table = 't_safe'
        verbose_name = '안전 자료'
        verbose_name_plural = '안전 자료 목록'
    
    def __str__(self):
        return f'[{self.id}:{self.s_title}]'
    

class SafeTag(models.Model):
    safe = models.ForeignKey(Safe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_safe_tag'
        verbose_name = '안전자료실 태그 연결'
        verbose_name_plural = '안전자료실 태그 연결 목록'
        
        constraints = [
        models.UniqueConstraint(fields=['safe', 'tag'], name='unique_safe_tag')
    ]

    def __str__(self):
        return f'{self.safe.s_title} - {self.tag.st_tag}'
    

class History(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='회원번호')
    safe = models.ForeignKey(Safe, on_delete=models.CASCADE, verbose_name='안전자료 번호')
    h_vdate = models.DateTimeField(auto_now=True, verbose_name='방문일시')

    class Meta:
        db_table = 't_history'
        verbose_name = '안전자료 방문기록'
        verbose_name_plural = '안전자료 방문기록(들)'
        ordering = ['-h_vdate']
        
       
        constraints = [
            models.UniqueConstraint(fields=['member', 'safe'], name='unique_member_safe')
        ]

    def __str__(self):
        return f'{self.member.m_name} - {self.safe.s_title} 방문'
    


    

