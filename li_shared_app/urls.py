from django.urls import path

from li_shared_app import views

urlpatterns = [
    path("prijava/", views.LoginView.as_view(), name="login"),
    path("registracija/", views.RegisterView.as_view(), name="register"),
    path("odjava/", views.LogoutView.as_view(), name="logout"),
    path("close/", views.CloseView.as_view(), name="close"),
]
