from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Member
from django.core.validators import EmailValidator

class Step1MemberForm(forms.Form):
    m_username = forms.CharField()
    m_password1 = forms.CharField(widget=forms.PasswordInput)
    m_password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_m_username(self):
        m_username = self.cleaned_data.get('m_username')
        if Member.objects.filter(m_username=m_username).exists():
            raise forms.ValidationError("이미 존재하는 아이디입니다.")
        return m_username

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("m_password1") != cleaned.get("m_password2"):
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return cleaned

class Step2MemberForm(forms.ModelForm):
    # 이메일과 전화번호를 위한 추가 필드
    email = forms.CharField(max_length=50, required=False)
    email_dns = forms.CharField(max_length=50, required=False)
    cel1 = forms.CharField(max_length=3, required=False)
    cel2_1 = forms.CharField(max_length=4, required=False)
    cel2_2 = forms.CharField(max_length=4, required=False)

    class Meta:
        model = Member
        # m_phone과 m_email은 save 메서드에서 직접 처리하므로 fields에서 제외
        fields = ["m_name", "m_birth_date", "m_address", "m_jaddress", "m_sex"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # m_name 필드의 유효성 검사 속성을 모델에서 가져와 위젯에 추가
        m_name_field = Member._meta.get_field('m_name')
        
        # maxlength 속성 설정
        max_length = m_name_field.max_length
        self.fields['m_name'].widget.attrs['maxlength'] = max_length
        
        # pattern 속성 설정 (RegexValidator가 있는 경우)
        # validator.regex는 정규식 객체이므로 .pattern으로 문자열을 가져옵니다.
        for validator in m_name_field.validators:
            if hasattr(validator, 'regex'):
                self.fields['m_name'].widget.attrs['pattern'] = validator.regex.pattern
                break  # 첫 번째 RegexValidator만 사용

        # 인스턴스가 있는 경우 (수정 시) 필드 초기값 설정
        if self.instance and self.instance.pk:
            # 이메일 분리
            if self.instance.m_email:
                try:
                    email_part, email_dns = self.instance.m_email.split('@')
                    self.initial['email'] = email_part
                    self.initial['email_dns'] = email_dns
                except (ValueError, AttributeError):
                    pass  # 이메일 형식이 올바르지 않거나 None일 경우
            # 전화번호 분리
            if self.instance.m_phone and len(self.instance.m_phone) == 11:
                self.initial['cel1'] = self.instance.m_phone[:3]
                self.initial['cel2_1'] = self.instance.m_phone[3:7]
                self.initial['cel2_2'] = self.instance.m_phone[7:]

            # 생년월일 필드 값을 명시적으로 초기화
            if self.instance.m_birth_date:
                self.initial['m_birth_date'] = self.instance.m_birth_date

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_dns = cleaned_data.get('email_dns')
        
        # 사용자가 이메일 필드를 둘 다 입력한 경우에만 검증
        if email and email_dns:
            m_email = f"{email}@{email_dns}"
            try:
                EmailValidator()(m_email)
            except forms.ValidationError:
                self.add_error('email', "유효한 이메일 주소를 입력해주세요.")

        return cleaned_data

    def save(self, commit=True):
        # 부모 save()를 호출하여 기본 필드들로 인스턴스를 가져옴
        instance = super().save(commit=False)

        # 이메일 처리
        email = self.cleaned_data.get('email')
        email_dns = self.cleaned_data.get('email_dns')
        if email and email_dns:
            instance.m_email = f"{email}@{email_dns}"
        else:
            # 사용자가 필드를 비웠다면 이메일 정보도 비움
            instance.m_email = None

        # 전화번호 처리
        cel1 = self.cleaned_data.get('cel1')
        cel2_1 = self.cleaned_data.get('cel2_1')
        cel2_2 = self.cleaned_data.get('cel2_2')
        if cel1 and cel2_1 and cel2_2:
            instance.m_phone = f"{cel1}{cel2_1}{cel2_2}"
        else:
            # 사용자가 필드를 비웠다면 전화번호 정보도 비움
            instance.m_phone = None
        
        if commit:
            instance.save()
            
        return instance