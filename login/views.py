from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from . import models, forms
import hashlib
from datetime import datetime, timedelta

def str2hash(string, salt='site1'):
    '''用hash函数加密密码'''
    m = hashlib.sha256()
    m.update((string+salt).encode())
    return m.hexdigest()

def make_activate_code(user):
    '''生成激活码'''
    now = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    code = str2hash(user.name, now)
    models.ActivateString.objects.create(code=code, user=user)
    return code

def send_mail(email_addr, code):
    '''发送注册带激活码链接的邮件'''
    subject = 'Site1 Demo的注册用户激活邮件'
    text_content = '感谢您注册了site1，请前往http://localhost:8000/activate/?code={}激活用户，该链接有效期{}天内有效'.format(
        code, settings.CONFIRM_DAYS)
    html_content = '<p>感谢您注册了site1，请前往<a href="http://localhost:8000/activate?code={}">' \
                   'http://localhost:8000/activate/?code={}</a>激活用户，该链接有效期{}天内有效</p>'.format(
        code, code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email_addr])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Create your views here.
def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    '''
    用户登陆视图函数
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
                if user.password == str2hash(password):
                    if user.has_activated == True:
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name
                        return redirect('/index/')
                    else:
                        message = '用户账号尚未激活，请前往注册邮箱，进行注册激活'
                else:
                    message = '密码不正确'
            except:
                message = '用户名不存在'
        return render(request, 'login/login.html', {'message':message, 'login_form':login_form})
    login_form = forms.UserForm()
    return render(request, 'login/login.html', {'login_form':login_form})

def register(request):
    '''
    用户注册视图函数
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
                new_user.password = str2hash(password)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                # 生成注册激活码，并发送带有激活链接的邮件到注册邮箱
                code = make_activate_code(new_user)
                send_mail(new_user.email, code)
                message = '已注册，请前往注册邮箱，进行注册激活'

        return render(request, 'login/register.html', {'message':message, 'register_form':register_form})

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', {'register_form':register_form})

def activate(request):
    '''
    用户激活视图函数
    :param request:
    :return:
    '''
    code = request.GET.get('code', None)
    message = ''
    try:
        activate_user = models.ActivateString.objects.get(code=code)
    except:
        message = '无效的激活请求'
        return render(request, 'login/activate.html', {'message':message})

    c_time = activate_user.c_time
    now = datetime.now()
    if activate_user.user.has_activated == True:
        message = '{}用户已经激活过了，不需要再次激活'.format(activate_user.user.name)
    elif now - c_time > timedelta(settings.CONFIRM_DAYS):
        activate_user.user.delete()
        activate_user.delete()
        message = '激活时效已过期，请重新注册用户并激活'
    else:
        activate_user.user.has_activated = True
        activate_user.user.save()
        message = '{}用户你好！账号已激活，请登录使用'.format(activate_user.user.name)

    return render(request, 'login/activate.html', {'message':message})


def logout(request):
    '''
    用户登出视图函数
    :param request:
    :return:
    '''
    if request.session.get('is_login', None):
        request.session.flush()
    return redirect('/index/')