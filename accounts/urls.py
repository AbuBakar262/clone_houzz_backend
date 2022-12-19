from django.urls import path
from accounts.view.user_management import SignupView, ProUserListView, ClientUserListView, LoginView, CreateProfile, Verify
from accounts.view.project_views import CreateProjectViewSet, UpdateDeleteProjectViewSet, ListProjectViewSet
from accounts.view.company_views import CreateCompanyViewSet, ListCompanyViewSet, UpdateDeleteCompanyViewSet

urlpatterns = [
    #user_views
    path("signup", SignupView.as_view({"post": "signup_view"}), name="signup"),
    path("pro_user_list", ProUserListView.as_view({"get": "pro_user_list"}), name="pro_user_list"),
    path("client_user_list", ClientUserListView.as_view({"get": "client_user_list"}), name="client_user_list"),
    path("create_profile/<str:pk>", CreateProfile.as_view({"put": "create_profile"}), name="create_profile"),
    path("login", LoginView.as_view({"post": "login"}), name="login"),

    #project_views
    path('create_project', CreateProjectViewSet.as_view({"post": "create"}), name="create_project"),
    path('list_projects', ListProjectViewSet.as_view({"get": "list"}), name="list_projects"),
    path('update_project/<str:pk>', UpdateDeleteProjectViewSet.as_view({"put": "update"}), name="update_project"),
    path('delete_project/<str:pk>', UpdateDeleteProjectViewSet.as_view({"delete": "destroy"}), name="delete_project"),

    #company_views
    path('create_company', CreateCompanyViewSet.as_view({"post": "create"}), name="create_company"),
    path('list_companies', ListCompanyViewSet.as_view({"get": "list"}), name="list_companies"),
    path('update_company/<str:pk>', UpdateDeleteCompanyViewSet.as_view({"put": "update"}), name="update_company"),
    path('delete_company/<str:pk>', UpdateDeleteCompanyViewSet.as_view({"delete": "destroy"}), name="delete_company"),

    #verify_email_and_phone
    path('otp_email', Verify.as_view({'post': 'otp_email'}), name='otp_email'),
    path('verify_otp', Verify.as_view({'post': 'verify_otp'}), name='verify_otp'),
    path('otp_phone', Verify.as_view({'post': 'otp_phone'}), name='otp_phone'),
]