from django.contrib import auth
from django.shortcuts import redirect, render

from main.forms import SignUpForm

# Create your views here.


def index(request):
    return render(request, "main/index.html")


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            # モデルフォームは form の値を models にそのまま格納できる
            form.save()

            # フォームから username と password を読み取る
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)


def login(request):
    return render(request, "main/login.html")
