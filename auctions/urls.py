from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("winning-lot", views.winning_lots, name="winning_lots"),
    path("my-list", views.my_list, name="my-list"),
    path("watching-list", views.watching_list, name="watching-list"),
    path("add", views.add, name="add"),
    path("add_to_watchlist/<int:auction_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("add_comment/<int:auction_id>", views.add_comment, name="add_comment"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("remove_from_watchlist/<int:auction_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("detail/<int:auction_id>", views.detail, name="detail"),
    path("delete/<int:auction_id>", views.delete, name="delete"),
    path("edit/<int:auction_id>", views.edit, name="edit"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
