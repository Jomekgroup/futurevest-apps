from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.investor_signup, name='investor_signup'),
    path('login/', views.investor_login, name='investor_login'),
    path('logout/', views.investor_logout, name='investor_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('invest/', views.invest, name='invest'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('test/', views.test_filter, name='test_filter'),
]
