from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required



def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')

        if password != password2:
            return render(request, 'accounts/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '' or email == '':
                return render(request, 'accounts/signup.html', {'error': '공백란이 있습니다.'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'accounts/signup.html', {'error': '계정이 존재합니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
                return redirect('/sign-in')


def sign_in_view(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'accounts/signin.html', {'error': '이름 혹은 패스워드를 확인 해 주세요.'})
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'accounts/signin.html')


@login_required
def logout(request):
    all_product = UserModel.objects.all()

    auth.logout(request)
    return redirect("/")
