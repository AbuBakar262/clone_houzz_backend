from import_modules import *
from idea_book.models import IdeaBook
from idea_book.serializers import CreateIdeaBookSerializer, ListIdeaBookSerializer, UpdateDeleteIdeaBookSerializer


class CreateIdeaBookViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = CreateIdeaBookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "Idea Created Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            idea_book = IdeaBook.objects.all()
            serializer = ListIdeaBookSerializer(idea_book, many=True)
            return Response({
                "success": True,
                "message": "Idea Book List",
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
            id  = kwargs.get('pk')
            idea_book = IdeaBook.objects.filter(id=id)
            idea_book.delete()
            return Response({
                "success": True,
                "message": "Idea Book Deleted Successfully",
                "data": ""
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk')
            idea_book = IdeaBook.objects.filter(id=id)
            serializer = UpdateDeleteIdeaBookSerializer(idea_book, many=True)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "Idea Book Updated Successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
