from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('update/<str:x>', views.update, name="update"),
    path('delete/<str:y>', views.delete, name="delete"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
]