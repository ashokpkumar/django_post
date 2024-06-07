from django.contrib import admin
from django.urls import path

from post_man.views import (
    PostManView,
    AuthView,
    Logout,
    Delivery,
    Delivered,
    NotReachable,
    Damaged,
    CsRejected,
    AddOrder,
    AddUser,
    ResetOrder,
    DeleteOrder,
)

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
    path("reset_order", ResetOrder.as_view(), name="reset_order"),
    path("delete_order", DeleteOrder.as_view(), name="reset_order"),
    path("insert_order/<street>/<landmark>/<city>/<state>/<country>", AddOrder.as_view(), name="reset_order"),
]
