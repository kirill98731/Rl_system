from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from .data_work import data_send
import datetime


def start_page(request):
    if '_auth_user_id' not in request.session.keys():
        log = False
    else:
        log = User.objects.get(id=request.session['_auth_user_id'])
    data = {}
    if log:
        data = data_send(datetime.datetime.now())
    data['log'] = log
    return render(request, 'rl_site/start_page.html', data)


def log(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user and user.is_active == True:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'rl_site/log.html', {'message': 'Неверный логин или пароль'})
    return render(request, 'rl_site/log.html')


def sign(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(username=request.POST['user'], password=request.POST['pass'])
            user.save()
        except:
            return render(request, 'rl_site/sign.html', {'message': 'Данный пользователь уже зарегистрирован'})
        return redirect('/login')
    return render(request, 'rl_site/sign.html')


def out(request):
    logout(request)
    return redirect('/')