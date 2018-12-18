from django import forms

from bbs_blog import models


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label = "用户名",
        error_messages={
            'max_length':'用户名不能超过16位',
            'required':"用户名不能为空"
        },
        widget=forms.widgets.TextInput(
            attrs={'class':'form-control'}
        )

    )
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,# 保留提交的值
        ),
        error_messages={
            "min_length": "密码至少需要6位！",
            "required": "密码不能为空",
        }
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        ),
        error_messages={
            "min_length": "确认密码至少要6位！",
            "required": "确认密码不能为空",
        }
    )