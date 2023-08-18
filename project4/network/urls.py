
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("perfil/<str:user_perfil>", views.perfil, name="perfil"),
    path("following/", views.following, name="following"),
    path("editPost/<int:id>/<str:new_value>", views.editPost, name="editPost"),



]
