from accounts.serializers import CreateProjectSerializer, ListProjectSerializer, UpdateDeleteProjectSerializer
from import_modules import *
from accounts.models import User, Projects


class CreateProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(role='Professional')

    def create(self, request, *args, **kwargs):
        try:
            serializer = CreateProjectSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "Project Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


class ListProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(role='Professional')

    def list(self, request, *args, **kwargs):
        try:
            queryset = Projects.objects.all()
            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = ListProjectSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateDeleteProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(role='Professional')

    def update(self, request, *args, **kwargs):
        try:
            queryset = Projects.objects.get(id=kwargs['pk'])
            serializer = UpdateDeleteProjectSerializer(queryset, data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "Project Updated Successfully",
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
            queryset = Projects.objects.get(id=kwargs['pk'])
            if Projects.objects.filter(id=kwargs['pk']).exists():
                queryset.delete()
                return Response({
                    "success": True,
                    "message": "Project Deleted Successfully",
                    "data": ""
                }, status=status.HTTP_200_OK)
            return Response({
                "success": False,
                "message": "Project Not Found",
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
