from django import forms
from django.forms import widgets
from blog.models import UserInfo
from django.core.exceptions import ValidationError  # 合法性错误


class User(forms.Form):
    # 用户名 密码 确认密码 邮箱
    username = forms.CharField(max_length=8, min_length=3, label='用户名', required=True,
                               error_messages={'max_length': '用户名最多只能输入8位',
                                               'min_length': '用户名最少输入3位',
                                               'required': '用户名必须填'
                                               },
                               widget=widgets.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(max_length=16, min_length=8, required=True, label='密码',
                               error_messages={
                                   'max_length': '密码最长16位',
                                   'min_length': '密码最短8位',
                                   'required': '密码不能为空',
                               },
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'})
                               )
    re_password = forms.CharField(max_length=16, min_length=8, required=True, label='密码',
                                  error_messages={
                                      'max_length': '密码最长16位',
                                      'min_length': '密码最短8位',
                                      'required': '密码不能为空',
                                  },
                                  widget=widgets.PasswordInput(attrs={'class': 'form-control'})
                                  )
    email = forms.EmailField(label='邮箱地址', widget=widgets.EmailInput(attrs={'class': 'form-control'}))

    # 局部钩子 校验用户名是否存在
    def clean_username(self):
        name = self.cleaned_data.get('username')
        if UserInfo.objects.filter(username=name).first():
            # 用户已存在
            raise ValidationError('用户名已存在')  # 校验错误抛出异常
        else:
            return name

    # 局部钩子 校验用户名是否存在
    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     try:
    #         UserInfo.objects.get(username=username)
    #         print(UserInfo.objects.get(username=username), type(UserInfo.objects.get(username=username)))
    #         raise ValidationError('用户名已存在')
    #     except Exception:
    #         return username

    # 全局钩子 校验两次输入密码是否一致
    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd != re_pwd:
            raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data
