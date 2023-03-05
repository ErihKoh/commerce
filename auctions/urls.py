from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my-list", views.my_list, name="my-list"),
    path("watching-list", views.watching_list, name="watching-list"),
    path("add", views.add, name="add"),
    path("detail/<int:auction_id>", views.detail, name="detail"),
    path("delete/<int:auction_id>", views.delete, name="delete"),
    path("edit/<int:auction_id>", views.edit, name="edit"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
