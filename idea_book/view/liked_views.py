from import_modules import *
from idea_book.models import Like
from idea_book.serializers import CreateLikeSerializer, ListLikeSerializer


class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = CreateLikeSerializer(data=request.data, context={'request': request})

            if not serializer.is_valid():
                return Response({
                    "success": False,
                    "message": serializer.errors,
                    "data": ""
                }, status=status.HTTP_400_BAD_REQUEST)

            liked_by = serializer.validated_data['liked_by']
            liked_on = serializer.validated_data['liked_on']
            liked = serializer.validated_data['liked']

            if Like.objects.filter(liked_by=liked_by, liked_on=liked_on).exists():
                like = Like.objects.get(liked_by=liked_by, liked_on=liked_on)
                like.liked = liked
                like.save()
                if liked is True:
                    return Response({
                        "success": True,
                        "message": "Idea Book Liked Successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "success": True,
                        "message": "Idea Book Dis-liked Successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
            serializer.save()
            return Response({
                "success": True,
                "message": "Idea Book Liked Successfully",
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
            idea_book_id = self.request.query_params["idea_book"]
            idea_book_likes = Like.objects.filter(liked_on=idea_book_id, liked=True)
            total_likes = idea_book_likes.count()
            serializer = ListLikeSerializer(idea_book_likes, many=True)
            return Response({
                "success": True,
                "message": "Idea Book Likes Listed Successfully",
                "data": {
                    "data": serializer.data,
                    "total_likes": total_likes
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "data": ""
            }, status=status.HTTP_400_BAD_REQUEST)
