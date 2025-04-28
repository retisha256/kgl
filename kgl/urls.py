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
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',auth_views.LoginView.as_view(template_name='login.html'),name="login"),
    path('dash/',views.dash,name='dash'),
     path('addstock/<str:pk>/',views.addstock, name="addstock") , 
     path('login/',views.Login, name="Login"),
    path('addsales/',views.addsales,name='addsales'),
    path('allstock/',views.allstock,name='allstock'),
   
    path ('signup/', views.signup, name="signup"),
    path('issue_item/<str:pk>/',views.issue_item, name ='issue_item'),
    path('allstock/<int:stock_id>/', views.detail, name="detail"),
    path('allsales/',views.allsales,name='allsales'),
    path("receipt/<int:receipt_id>/",views.receipt_detail, name="receipt_detail"),
    path('allstock/',views.allstock,name='allstock'),
    path('addcredit/',views.addcredit,name='addcredit'),
    path('receipt/',views.receipt,name='receipt'),
    path('dashboard1/',views.salesagent,name="salesagent"),
    path('dashboard1/',views.manager,name="manager"),
   path ('dashboard1/',views.owner,name="owner"),

    

]
