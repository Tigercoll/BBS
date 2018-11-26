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