from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Member

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
    class Meta:
        model = Member
        fields = ["m_name", "m_birth_date", "m_address", "m_jaddress", "m_phone", "m_email", "m_sex"]
        