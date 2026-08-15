from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from representations.serializers.Representation_serializer import RepresentationSerializer
from representations.services.representation_service import RepresentationService

class RepresentationView():
    
    @staticmethod
    @api_view(["GET"])
    def search_all():
        repre_service = RepresentationService()
        try:
            repres = repre_service.find_all_active()
            serializer = RepresentationService(repres, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    