from django.urls import path
from .views import CustomLoginView, register_view, logout_view

app_name = 'login'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
