from django.shortcuts import render, redirect
from . import models, forms
import hashlib

def password2hash(password):
    '''用hash函数加密密码'''
    m = hashlib.sha256()
    m.update((password+'site1').encode())
    return m.hexdigest()

# Create your views here.
def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    '''
    登陆视图函数
    :param request:
    :return:
    '''
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password2hash(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = '密码不正确'
            except:
                message = '用户名不存在'
        return render(request, 'login/login.html', {'message':message, 'login_form':login_form})
    login_form = forms.UserForm()
    return render(request, 'login/login.html', {'login_form':login_form})

def register(request):
    '''
    注册视图函数
    :param request:
    :return:
    '''
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            confirm_password = register_form.cleaned_data['confirm_password']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            # 在数据库中取输入的用户名和邮箱，判断是否已存在
            same_user = models.User.objects.filter(name=username)
            same_email = models.User.objects.filter(email=email)
            if same_user:
                message = '该用户名已注册，请换另一个用户名进行注册'
            elif password != confirm_password:
                message = '第2次输入的确认密码不正确，请重新输入密码'
            elif same_email:
                message = '该邮箱已注册，请换另一个邮箱进行注册'
            else:
                new_user = models.User()
                new_user.name = username
                new_user.password = password2hash(password)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')

        return render(request, 'login/register.html', {'message':message, 'register_form':register_form})

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', {'register_form':register_form})

def logout(request):
    '''
    登出视图函数
    :param request:
    :return:
    '''
    if request.session.get('is_login', None):
        request.session.flush()
    return redirect('/index/')