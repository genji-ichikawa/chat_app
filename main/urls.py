from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("friends/", views.friends, name="friends"),
    path("talk_room/<int:friend_id>/", views.talk_room, name="talk_room"),
    path("settings/", views.settings, name="settings"),
]
