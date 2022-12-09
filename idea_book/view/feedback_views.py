from import_modules import *
from idea_book.models import FeedBack, IdeaBook
from idea_book.serializers import CreateFeedbackSerializer, ListFeedbackSerializer, UpdateFeedBackSerializer


class FeedBackViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = CreateFeedbackSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "FeedBack Created Successfully",
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
            user_id = request.user.id
            feedback = FeedBack.objects.filter(feedback_on__user=user_id)
            serializer = ListFeedbackSerializer(feedback, many=True)
            return Response({
                "success": True,
                "message": "Feedback List",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            feedback = FeedBack.objects.get(id=pk)
            serializer = UpdateFeedBackSerializer(feedback, data=request.data)
            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "success": True,
                "message": "FeedBack Updated Successfully",
                "data": serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            feedback = FeedBack.objects.get(id=pk)
            feedback.delete()
            return Response({
                "success": True,
                "message": "FeedBack Deleted Successfully",
                "data": ""
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            },status=status.HTTP_400_BAD_REQUEST)
