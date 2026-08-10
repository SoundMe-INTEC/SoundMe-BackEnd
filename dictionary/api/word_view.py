from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from dictionary.services.word_service import WordService
from dictionary.serializers.word_serializer import WordSerializer


class WordView():
    
    @staticmethod
    @api_view(["GET"])
    def get_all(request):
        word_service = WordService()
        try:
            words = word_service.find_all_active()
            serializer = WordSerializer(words, words=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @api_view(["GET"])
    def get(request):
        word_service = WordService()
        word_name = request.query_params.get("word_name")
        if not word_name:
            return Response(
                {"detail": "word_name query parameter is required "},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            word = word_service.find_by_word_name(word_name)
            serializer = WordSerializer(word, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)