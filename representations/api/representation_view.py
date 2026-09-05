from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from representations.serializers.Representation_serializer import RepresentationSerializer
from representations.services.representation_service import RepresentationService
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from config.pagination import AdminResultsPagination


class RepresentationView:

    @staticmethod
    @api_view(["GET"])
    @permission_classes([AllowAny])

    def search_all(request):
        representation_service = RepresentationService()
        try:
            representations = representation_service.find_all_active()
            serializer = RepresentationSerializer(representations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([AllowAny])

    def get(request):
        representation_service = RepresentationService()
        sign_id = request.query_params.get("sign_id")
        if not sign_id:
            return Response({"detail": "sign_id query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            representation = representation_service.find_by_id(sign_id)
            serializer = RepresentationSerializer(representation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    @permission_classes(IsAuthenticated) # type: ignore

    def create(request):
        representation_service = RepresentationService()
        serializer = RepresentationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            representation = representation_service.create(
                serializer.validated_data,
                request.user,
                request.data.get("sign_id"),
            )
            return Response({"representation": str(representation.id)}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([IsAdminUser])
    def list_admin(request):
        representation_service = RepresentationService()
        representations = representation_service.find_all().order_by("sign_id", "order")

        sign_id = request.query_params.get("sign_id")
        if sign_id:
            representations = representations.filter(sign_id=sign_id)

        paginator = AdminResultsPagination()
        page = paginator.paginate_queryset(representations, request)
        serializer = RepresentationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    @api_view(["PATCH"])
    @permission_classes([IsAdminUser])
    def update(request, representation_id):
        representation_service = RepresentationService()
        try:
            representation = representation_service.update_by_pk(representation_id, request.data)
            return Response(RepresentationSerializer(representation).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def deactivate(request, representation_id):
        representation_service = RepresentationService()
        try:
            representation = representation_service.deactivate(representation_id)
            return Response(RepresentationSerializer(representation).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def activate(request, representation_id):
        representation_service = RepresentationService()
        try:
            representation = representation_service.activate(representation_id)
            return Response(RepresentationSerializer(representation).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)