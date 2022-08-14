"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('records/', views.records, name='records'),
    path('addrecord/', views.addrecord, name='addrecord'),
    path('updaterecord/<str:pk>/', views.updaterecord, name='updaterecord'),
    path('notifications/', views.notifications, name='notifications'),
    path('reports/', views.reports, name='reports'),
    path('reports/generatepdf', views.generatepdf, name='generatepdf'),
    path('generateall/', views.generateall, name='generateall'),
    path('about/', views.about, name='about'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    
]
