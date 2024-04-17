from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app.models import users


@csrf_exempt
def index(request):
    if request.method == 'POST':
        login = request.POST['login']
        email = request.POST['email']
        for i in users.objects.all():
            if i.email == email:
                return render(request, 'index.html', {'msg': 'Данный Email занят!'})
            if i.login == login:
                return render(request, 'index.html', {'msg': 'Данный логин занят!'})
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
            for user in users.objects.all():
                if user.login == login and user.password == password:
                    html = redirect('/profile/')
                    html.set_cookie('user_login', user.login)
                    html.set_cookie('user_email', user.email)
                    html.set_cookie('isAuth', 'true')
                    return html
            return render(request, 'login.html', {'msg': 'Неверный логин или пароль'})
        return render(request, 'login.html')


@csrf_exempt
def profile(request):
    if request.method == 'POST':
        html = redirect('/login/')
        html.delete_cookie('isAuth')
        return html
    try:
        if request.COOKIES.get('isAuth') == 'true':
            current_user_login = request.COOKIES.get('user_login')
            current_user_email = request.COOKIES.get('user_email')

            return render(request, 'profile.html', {'login': current_user_login, 'email': current_user_email})
    except:
        return redirect('/login/')
