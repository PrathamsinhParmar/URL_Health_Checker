from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('urls/add/', views.add_url, name='url_add'),
    path('urls/<int:pk>/edit/', views.edit_url, name='url_edit'),
    path('urls/<int:pk>/delete/', views.delete_url, name='url_delete'),
    path('urls/<int:pk>/', views.url_detail, name='url_detail'),
    path('accounts/register/', views.register, name='register'),
]
