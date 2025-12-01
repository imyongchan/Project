from django.db import models

class News(models.Model):
    n_title = models.CharField(max_length=150, verbose_name='뉴스제목')
    n_writer = models.CharField(max_length=100, null=True, verbose_name='뉴스작성자')
    n_contents = models.CharField(max_length=500, verbose_name='뉴스내용')
    n_link = models.CharField(max_length=1000, verbose_name='뉴스링크')
    n_image_url = models.CharField(max_length=255, verbose_name='뉴스이미지')
    n_created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='뉴스작성일')

    class Meta:
        db_table = 't_news'
        verbose_name = '뉴스'
        verbose_name_plural = '뉴스 목록'
    
    def __str__(self):
        return f'[{self.id}:{self.n_title}]'