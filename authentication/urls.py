"""
URL configuration for gfg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('signup' ,views.signup,name="signup"),
    path('signin' ,views.signin ,name="signin"),
    path('signout', views.signout ,name="signout"),
    path('dashboard', views.dashboard ,name="dashboard"),
    path('addform', views.addform ,name="addform"),
    path('edit/<int:pk>/' ,views.edit_object , name ="edit_object"),
    path('delete/<int:pk>/' ,views.delete_object , name ="delete_object"),
    path('deactivate/<int:pk>/' ,views.deactivate_item , name ="deactivate_item"),
    path('activate/<int:pk>/' ,views.activate_item , name ="activate_item"),
    path("drivers" , views.drivers ,name="drivers"),
    path("calculation_price_api" , views.calculation_price_api ,name="calculation_price_api"),
     path('download/', views.download_page, name='download_page'),
    path('generate-and-download-csv/', views.generate_and_download_csv, name='generate_and_download_csv'),
    path('download-combined-csv/', views.download_combined_csv, name='download_combined_csv'),
]

