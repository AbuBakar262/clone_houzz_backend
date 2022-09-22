from django.urls import path
from accounts.view.user_management import SignupView, ProUserListView, ClientUserListView, UpdateDeleteUserView, \
    LoginView

urlpatterns = [
    path("signup/", SignupView.as_view({"post": "signup_view"}), name="signup"),
    path("pro_user_list/", ProUserListView.as_view({"get": "pro_user_list"}), name="pro_user_list"),
    path("client_user_list/", ClientUserListView.as_view({"get": "client_user_list"}), name="client_user_list"),
    path("update/<str:pk>/", UpdateDeleteUserView.as_view({"update": "put"}), name="update_pro_user"),
    path("login/", LoginView.as_view({"post": "login"}), name="login")
]