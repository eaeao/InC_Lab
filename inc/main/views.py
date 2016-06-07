from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from inc.main.models import UserProfile


def main(request):
    context = {
        'user':request.user,
        'appname': 'main'
    }
    return render(request, 'main.html', context)

def auth_login(request):
    if request.user.id :
        return HttpResponseRedirect("/")
    email = request.POST.get("email")
    if email :
        password = request.POST.get("password")
        login_from = request.POST.get("from", '/')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            request.session.set_expiry(31536000)
            return HttpResponseRedirect(login_from)
        return HttpResponseRedirect("/auth/login/?from=%s&msg=403"%login_from)
    else :
        login_from = request.GET.get('from')
        msg = request.GET.get('msg')
        context = {
            'user': request.user,
            'from':login_from,
            'msg':msg,
            'appname': 'login'
        }
        return render(request, 'login.html', context)

def auth_register(request):
    if request.user.id :
        return HttpResponseRedirect("/")
    email = request.POST.get("email")
    if email :
        password = request.POST.get("password")
        username = request.POST.get("username")
        grade = request.POST.get("grade")

        try:
            user = User.objects.create_user(username=email, password=password, email=email, first_name=username)
            if user:
                profile = UserProfile.objects.create(user=user, grade=grade)
                user = authenticate(username=email, password=password)
                if user:
                    login(request, user)
                    request.session.set_expiry(31536000)
                    return HttpResponseRedirect('/')
        except Exception as e:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else :
        context = {
            'user': request.user,
            'appname': 'register'
        }
        return render(request, 'register.html', context)

def auth_logout(request):
    login_from = request.POST.get("from", '/')
    logout(request)
    return HttpResponseRedirect(login_from)

def JudgeOnline(request):
    return HttpResponseRedirect("http://163.152.112.7:8080/JudgeOnline")