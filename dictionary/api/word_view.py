from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from dictionary.services.word_service import WordService
from dictionary.serializers.word_serializer import WordSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from config.pagination import AdminResultsPagination


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

    @staticmethod
    @api_view(["GET"])
    @permission_classes([IsAdminUser])
    def list_admin(request):
        word_service = WordService()
        words = word_service.find_all().order_by("word_name")

        search = request.query_params.get("search")
        if search:
            words = words.filter(word_name__icontains=search)

        paginator = AdminResultsPagination()
        page = paginator.paginate_queryset(words, request)
        serializer = WordSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    @api_view(["PATCH"])
    @permission_classes([IsAdminUser])
    def update(request, word_id):
        word_service = WordService()
        try:
            word = word_service.update_by_id(word_id, request.data)
            return Response(WordSerializer(word).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def deactivate(request, word_id):
        word_service = WordService()
        try:
            word = word_service.deactivate(word_id)
            return Response(WordSerializer(word).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def activate(request, word_id):
        word_service = WordService()
        try:
            word = word_service.activate(word_id)
            return Response(WordSerializer(word).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)