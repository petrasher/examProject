from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app.models import users


@csrf_exempt
def index(request):
    if request.method == 'POST':
        user = users()
        user.email = request.POST['email']
        user.login = request.POST['login']
        user.password = request.POST['password']
        user.save()

        return render(request, 'index.html', {'msg': 'Регистрация прошла успешно!'})
    return render(request, 'index.html', {'msg': 'Пожалуйста, зарегистрируйтесь!'})


@csrf_exempt
def login(request):
    try:
        if request.COOKIES['isAuth'] == 'true':
            return redirect('/profile/')
    except:
        if request.method == 'POST':
            login = request.POST['login']
            password = request.POST['password']
            for i in users.objects.all():
                if i.login == login and i.password == password:
                    html = redirect('/profile/')
                    html.set_cookie('isAuth', 'true')
                    return html
                return render(request, 'login.html', {'msg': 'Неверный логин или пароль'})
            return render(request, 'login.html')
        return render(request, 'login.html')


@csrf_exempt
def profile(request):
    if request.method == 'POST':
        html = redirect('/login/')
        html.delete_cookie('isAuth')
        return html
    try:
        if request.COOKIES['isAuth'] == 'true':
            return render(request, 'profile.html')
    except: return redirect('/login/')

