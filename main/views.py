from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "main/index.html")


def signup(request):
    return render(request, "main/signup.html")


def login(request):
    return render(request, "main/login.html")
