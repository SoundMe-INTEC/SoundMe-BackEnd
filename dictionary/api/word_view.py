from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from dictionary.services.word_service import WordService
from dictionary.serializers.word_serializer import WordSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class WordView():

    @staticmethod
    @api_view(["GET"])
    @permission_classes([AllowAny])
    
    def get_all(request):
        word_service = WordService()
        try:
            words = word_service.find_all_active()
            serializer = WordSerializer(words, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([AllowAny])

    def get(request):
        word_service = WordService()
        word_name = request.query_params.get("word_name")
        if not word_name:
            return Response(
                {"detail": "word_name query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            word = word_service.find_by_word_name(word_name)
            serializer = WordSerializer(word)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def create(request):
        word_service = WordService()
        serializer = WordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            word = word_service.create(
                serializer.validated_data,
                request.user
            )
            return Response(
                {"word": str(word.word_name)}, status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)