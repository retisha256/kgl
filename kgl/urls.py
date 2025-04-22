"""
URL configuration for kgl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from kgl_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('dash/',views.dash,name='dash'),
    path('addstock/',views.addstock,name='addstock'),
    path('addsales/',views.addsales,name='addsales'),
    path('allstock/',views.allstock,name='allstock'),
    path('allsales/',views.allsales,name='allsales'),
    path('addcredit/',views.addcredit,name='addcredit'),
    path('receipt/',views.receipt,name='receipt')

]
