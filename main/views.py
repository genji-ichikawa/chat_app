from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import LoginForm, SignUpForm, TalkForm
from main.models import Talk

User = get_user_model()


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


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    template_name = "main/login.html"


@login_required
def friends(request):
    friends = User.objects.exclude(id=request.user.id)
    context = {"friends": friends}
    return render(request, "main/friends.html", context)


@login_required
def talk_room(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)

    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        | Q(sender=friend, receiver=request.user)
    ).order_by("time")

    if request.method == "GET":
        form = TalkForm()
    elif request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            new_talk = form.save(commit=False)
            new_talk.sender = request.user
            new_talk.receiver = friend
            new_talk.save()
            return redirect("talk_room", friend_id)

    context = {
        "form": form,
        "friend": friend,
        "talks": talks,
    }
    return render(request, "main/talk_room.html", context)


@login_required
def settings(request):
    return render(request, "main/settings.html")
