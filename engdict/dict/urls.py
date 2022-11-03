from django.urls import path
from .views import index, delete, CustomLoginView, RegisterPage

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", index, name="index"),
    path("delete/<int:pk>/", delete, name="delete"),
]
