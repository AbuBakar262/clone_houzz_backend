from import_modules import *
from accounts.models import User, OtpVerification
from accounts.serializers import SignupSerializer, UserListSerializer, LoginSerializer, CreateProfileSerializer, \
    EmailVerifySerializer, OtpSerializer, PhoneVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


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


class CreateProfile(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def create_profile(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            user_id = kwargs.get('pk')
            if not User.objects.filter(id=user_id).exists():
                return Response({
                    "success": False,
                    "message": "User Not Found",
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            instance = self.get_object()
            serializer = CreateProfileSerializer(instance, data=request.data, partial=partial,
                                                     context={'instance': instance})
            if not serializer.is_valid():
                return Response({
                    "success": True,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response({
                "success": True,
                "message": "Profile Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save(create_profile=True, terms_conditions=True)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

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
            user_data = serializer.data
            user = User.objects.get(email=user_data.get("email"))
            if user.role == 'Client':
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
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


class Verify(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def otp_email(self, request, *args, **kwargs):
        try:
            serializer = EmailVerifySerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "OTP is send to your email, Check Your Email and Verify OTP",
                "data": ""
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def otp_phone(self, request, *args, **kwargs):
        try:
            serializer = PhoneVerifySerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "OTP is send to your phone, Check Your Phone and Verify OTP",
                "data": ""
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


    def verify_otp(self, request, *args, **kwargs):
        try:
            serializer = OtpSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            otp = serializer.validated_data.get("otp")
            verify_otp = OtpVerification.objects.get(otp=otp)
            user = User.objects.filter(id=verify_otp.otp_user.id)
            if verify_otp.email_verified is True:
                user.update(email_verified=True)
            user.update(phone_verified=True)
            verify_otp.delete()
            return Response({
                "success": True,
                "message": "OTP Verified Successfully",
                "data": ""
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
