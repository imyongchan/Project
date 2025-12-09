from django.db import models



class Stats1(models.Model): # 전체 재해 현황 및 분석- 업종별 
    dt          = models.FloatField()                 # DT(값)
    prd_de      = models.IntegerField()               # PRD_DE (연도)
    lst_chn_de  = models.DateField()                  # LST_CHN_DE(최종수정일)
    c1_nm       = models.CharField(max_length=150)    # C1_NM (업종명)
    itm_nm      = models.CharField(max_length=150)    # ITM_NM (재해자수, 재해율, ...)

    class Meta:
        db_table = 't_stats1'
        verbose_name = '업종별 재해 사망율 통계'


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.itm_nm} = {self.dt}"


class Stats2(models.Model): # 전체 재해 현황 및 분석- 성별 
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 남자/여자
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 성별

    class Meta:
        db_table = 't_stats2'
        verbose_name = "업종별 성별 통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"
    

class Stats3(models.Model): # 사망 재해 현황 및 분석- 성별
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 남자/여자
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM   
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 성별

    class Meta:
        db_table = 't_stats3'
        verbose_name = "업종별 성별 사망통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"
    

class Stats4(models.Model): # 전체 재해 현황 및 분석- 연령별
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 연령대
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 연령별

    class Meta:
        db_table = 't_stats4'
        verbose_name = "업종별 연령대 통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"
    



class Stats5(models.Model): # 사망재해 현황 및 분석- 연령별
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 연령대
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 연령별

    class Meta:
        db_table = 't_stats5'
        verbose_name = "업종별 연령대 사망통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"
    

class Stats6(models.Model): # 전체 재해 현황 및 분석- 발생형태별
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 발생형태
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 발생형태별

    class Meta:
        db_table = 't_stats6'
        verbose_name = "업종별 발생형태 통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"
    

class Stats7(models.Model): # 사망 재해 현황 및 분석- 발생형태별
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 발생형태
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 발생형태별

    class Meta:
        db_table = 't_stats7'
        verbose_name = "업종별 발생형태 사망통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"
    

class Stats8(models.Model): # 전체 재해 현황 및 분석- 세부질병
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 세부질병
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 세부질병별

    class Meta:
        db_table = 't_stats8'
        verbose_name = "업종별 세부질병 통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"


class Stats9(models.Model): # 전체 재해 현황 및 분석- 세부질병
    c1_obj_nm  = models.CharField(max_length=100)   # C1_OBJ_NM : 업종별 중분류
    c2_nm      = models.CharField(max_length=20)   # C2_NM     : 세부질병
    dt         = models.FloatField()               # DT        : 값(재해자수 등)
    prd_de     = models.IntegerField()             # PRD_DE    : 연도
    c1_nm      = models.CharField(max_length=100)  # C1_NM     : 업종명 (광업, 제조업 ...)
    itm_nm     = models.CharField(max_length=150)  # ITM_NM    
    c2_obj_nm  = models.CharField(max_length=50)   # C2_OBJ_NM : 세부질병별

    class Meta:
        db_table = 't_stats9'
        verbose_name = "업종별 세부질병 사망통계"


    def __str__(self):
        return f"{self.prd_de} / {self.c1_nm} / {self.c2_nm} = {self.dt}"