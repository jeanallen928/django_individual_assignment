from django.shortcuts import render, redirect


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/erp')
    else:
        return redirect('/sign-in')


def erp(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'erp/home.html')
        else:
            return redirect('/sign-in')
