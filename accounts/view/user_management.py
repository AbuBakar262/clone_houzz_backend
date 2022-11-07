from import_modules import *
from accounts.models import User
from accounts.serializers import SignupSerializer, UserListSerializer, UpdateDeleteProSerializer, LoginSerializer, \
    UpdateDeleteClientSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def update_response(user, request):
    if user.role == 'Professional':
        serializer = UpdateDeleteProSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": serializer.errors,
                "data": ''
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "success": True,
            "message": "Professional User Updated Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    if user.role == 'Client':
        serializer = UpdateDeleteClientSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": serializer.errors,
                "data": ''
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "success": True,
            "message": "Client User Updated Successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


def login_response(user):
    if user is None:
        return Response({
            "success": False,
            "message": "Username or Email is Invalid!",
            "data": ""
        }, status=status.HTTP_400_BAD_REQUEST)
    if user.role == "Client":
        return Response({
            "success": True,
            "message": "Client Logged in successfully",
            "data": {
                "access_token": str(AccessToken.for_user(user)),
                "refresh_token": str(RefreshToken.for_user(user)),
                "role": user.role,
                "email": user.email,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)
    elif user.role == 'Professional':
        return Response({
            "success": True,
            "message": "Professional Logged in successfully",
            "data": {
                "access_token": str(AccessToken.for_user(user)),
                "refresh_token": str(RefreshToken.for_user(user)),
                "role": user.role,
                "email": user.email,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)
    elif user.is_superuser is True:
        return Response({
            "success": True,
            "message": "Admin Logged in successfully",
            "data": {
                "access_token": str(AccessToken.for_user(user)),
                "refresh_token": str(RefreshToken.for_user(user)),
                "email": user.email,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "message": "Invalid email or password",
            "data": ""
        }, status=status.HTTP_400_BAD_REQUEST)


class DynamicPagination(pagination.PageNumberPagination):
    page_size = 10


class SignupView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def signup_view(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ''
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "User Created Successfully",
                "data": serializer.data,
            }, status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


class ProUserListView(viewsets.ModelViewSet):
    """
        View for getting Professional User List
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = DynamicPagination

    def pro_user_list(self, request):
        try:
            queryset = User.objects.filter(role='Professional')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = UserListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


class ClientUserListView(viewsets.ModelViewSet):
    """
        View for getting Client User List
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = DynamicPagination

    def client_user_list(self, request):
        try:
            queryset = User.objects.filter(role='Client')
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = UserListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteUserView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            return update_response(instance, request)
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': e.args[0],
                    'data': "",
                }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def login(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            email = serializer.validated_data.get("email")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")

            if email:
                user = User.objects.get(email=email)
                if user:
                    if user.check_password(password):
                        return login_response(user)
                    else:
                        return Response({
                            "success": False,
                            "message": "Invalid email or password",
                            "data": ""
                        }, status=status.HTTP_400_BAD_REQUEST)
            if username:
                user = User.objects.get(username=username)
                if user:
                    if user.check_password(password):
                        return login_response(user)
                    else:
                        return Response({
                            "success": False,
                            "message": "Invalid username or password",
                            "data": ""
                        }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
