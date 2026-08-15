from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from representations.serializers.Representation_serializer import RepresentationSerializer
from representations.services.representation_service import RepresentationService


class RepresentationView:

    @staticmethod
    @api_view(["GET"])
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