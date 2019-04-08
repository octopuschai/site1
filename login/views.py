from django.shortcuts import render, redirect
from . import models, forms

# Create your views here.
def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
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
                if user.password == password:
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
    pass
    return render(request, 'login/register.html')

def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
    return redirect('/index/')