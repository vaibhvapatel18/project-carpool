"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from app1 import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('page_register/', views.page_register, name='page_register'),
    path('page_login/', views.page_login, name='page_login'),
    path('page_otp/', views.page_otp, name='page_otp'),
    path('redirect/', views.redirect, name='redirect'),
    path('page_forget', views.page_forget, name='page_forget'),
    path('page_profile', views.page_profile, name='page_profile'),
    path('page_addblog/',views.addblog, name='addblog'),
    path('page_blogs/', views.viewblog, name='viewblog'),
    path('createride/', views.createride, name='createride'),
    path('reride/<int:pk>', views.reride, name='reride'),
    path('findride/', views.findride, name='allride'),
    path('bookride/<int:pk>', views.bookride, name='bookride'),
    path('myride/', views.myride, name='myride'),
    path('delete/<int:pk>/<int:ride_id>', views.delete, name='delete'),
    path('fire/<int:pk>/<int:ride_id>', views.fire, name='fire'),
    # path('remove/<int:ride_id>', views.remove, name='remove'),
    path('information/<int:pk>', views.information, name='information'),
    path('get/',views.UserList.as_view(),name='get'),
    path('post/', views.UserCreate.as_view(), name='post'),
    path('put/<int:pk>',views.UserPut.as_view(), name='put'),
    path('delete/<int:pk>',views.UserDelete.as_view(), name='delete'),



]
