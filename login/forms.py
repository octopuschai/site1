from django import forms

# 导入验证码库
from captcha.fields import CaptchaField

# from . import models

class UserForm(forms.Form):
    '''
    创建用户登陆表单类
    '''
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
    captcha = CaptchaField(label='验证码')

'''
使用Django model来构建form
class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['name', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, *kwargs)
        self.fields['name'].label = '用户名'
        self.fields['password'].label = '密码'
'''

class RegisterForm(forms.Form):
    '''
    创建用户注册表单类
    '''
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(label='确认密码', max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')