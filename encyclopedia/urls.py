from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display_entry, name="display_entry"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("edit/<str:title>", views.editPage, name="editPage"),
    path("randomPage", views.randomPage, name="randomPage")
]
