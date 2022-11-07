from import_modules import *
from accounts.models import User, Company
from accounts.serializers import CreateCompanySerializer, ListCompanySerializer, UpdateDeleteCompanySerializer


class CreateCompanyViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Company.objects.all()

    def create(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            if user.role == 'Professional':
                if Company.objects.filter(pro_user=user).exists():
                    return Response({
                        "success": False,
                        "message": "Company Already Exist"
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = CreateCompanySerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({
                            "success": True,
                            "message": "Company Created Successfully"
                        }, status=status.HTTP_201_CREATED)
                    else:
                        return Response({
                            "success": False,
                            "message": serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "success": False,
                    "message": "You are not a Professional"
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ListCompanyViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.all()

    def list(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            if user.role == 'Professional':
                queryset = Company.objects.filter(pro_user=user)
                paginator = PageNumberPagination()
                paginator.page_size = 10
                result_page = paginator.paginate_queryset(queryset, request)
                serializer = ListCompanySerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response({
                    "success": False,
                    "message": "You are not a Professional"
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteCompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            queryset = Company.objects.get(id=kwargs['pk'])
            serializer = UpdateDeleteCompanySerializer(queryset, data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "Company Updated Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            queryset = Company.objects.get(id=kwargs['pk'])
            if Company.objects.filter(id=kwargs['pk']).exists():
                queryset.delete()
                return Response({
                    "success": True,
                    "message": "Company Deleted Successfully",
                    "data": ""
                }, status=status.HTTP_200_OK)
            return Response({
                "success": False,
                "message": "Company Not Found",
                "data": ""
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
