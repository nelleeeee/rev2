from django import forms
from .models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
)

# 유저크리에션폼이 회원가입폼
class SignupForm(UserCreationForm):
    # 원래 이메일 필드는 false 인데 true로 바꿔주기
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    # 속성을 바꿔줘야 하는데 그냥 메타쓰면 사인업폼의 메타를 씀. 그래서 상속
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    # 이메일 중복 피하기
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 있는 이메일")
            return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "website_url",
            "bio",
            "phone_number",
            "gender",
        ]


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password")
        if old_password and new_password1:
            if old_password == new_password1:
                raise forms.ValidationError("새암호가 기존 암호와 같습니다.")
        return new_password1
