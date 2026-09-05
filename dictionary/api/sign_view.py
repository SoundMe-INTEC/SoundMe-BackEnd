from rest_framework.decorators import api_view, permission_classes
from dictionary.services.sign_service import SignService
from dictionary.serializers.sign_serializer import SignSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from config.pagination import AdminResultsPagination


class SignView():    
    @staticmethod
    @api_view(["GET"])
    @permission_classes([AllowAny])
    def get_all(request):
        sign_service = SignService()
        try:
            signs = sign_service.find_all_active()
            serializer = SignSerializer(signs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([AllowAny])
    def get(request):
        sign_service = SignService()
        sign_name = request.query_params.get("sign_name")
        if not sign_name:
            return Response(
                {"detail": "sign_name query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            sign = sign_service.find_by_sign_name(sign_name)
            serializer = SignSerializer(sign)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(["POST"])
    @permission_classes(IsAuthenticated) # type: ignore
    def create(request):
        sign_service = SignService()
        serializer = SignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            sign = sign_service.create(
                serializer.validated_data, 
                request.user
            )
            return Response(
                {"sign": str(sign.sign_name)}, status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([IsAdminUser])
    def list_admin(request):
        sign_service = SignService()
        signs = sign_service.find_all().order_by("sign_name")

        search = request.query_params.get("search")
        if search:
            signs = signs.filter(sign_name__icontains=search)

        paginator = AdminResultsPagination()
        page = paginator.paginate_queryset(signs, request)
        serializer = SignSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    @api_view(["PATCH"])
    @permission_classes([IsAdminUser])
    def update(request, sign_id):
        sign_service = SignService()
        try:
            sign = sign_service.update_by_id(sign_id, request.data)
            return Response(SignSerializer(sign).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def deactivate(request, sign_id):
        sign_service = SignService()
        try:
            sign = sign_service.deactivate(sign_id)
            return Response(SignSerializer(sign).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def activate(request, sign_id):
        sign_service = SignService()
        try:
            sign = sign_service.activate(sign_id)
            return Response(SignSerializer(sign).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)