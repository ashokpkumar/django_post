"""
URL configuration for post project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from post_man.views import PostManView, AuthView,\
    Logout,Delivery,Delivered,NotReachable,Damaged,\
        CsRejected,AddOrder,AddUser
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", PostManView.as_view(), name="postman"),
    path("authenticate", AuthView.as_view(), name="authenticate"),
    path("logout", Logout.as_view(), name="logout"),
    path("start", Delivery.as_view(), name="start"),

    path("delivered/<order_id>", Delivered.as_view(), name="delivered"),
    path("not_reachable/<order_id>", NotReachable.as_view(), name="not_reachable"),
    path("damaged/<order_id>", Damaged.as_view(), name="damaged"),
    path("cus_rejected/<order_id>", CsRejected.as_view(), name="cus_rejected"),

    path("add_user", AddUser.as_view(), name="AddUser"),
    path("add_order", AddOrder.as_view(), name="cus_rejected"),


]
