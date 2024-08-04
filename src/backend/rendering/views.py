from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def render_login(request):
    return render(request, 'login.html')
