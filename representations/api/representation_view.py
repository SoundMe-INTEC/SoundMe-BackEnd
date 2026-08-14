from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import request
from representations.serializers.Representation_serializer import RepresentationSerializer
from representations.services.representation_service import RepresentationService
from dictionary import models
    
class RepresentationView():
    
    @staticmethod
    @api_view(["GET"])
    def search_all():
        repre_service = RepresentationService()
        try:
            repres = repre_service.find_all_active()
            serializer = RepresentationSerializer(repres, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @api_view(["GET"])
    def search_one(request):
        repre_service = RepresentationService()
        sign_id = request.queryparams.get("sign_id")
        if not sign_id:
            return Response(
                {"detail": "sign_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            repres = repre_service.find_by_id(sign_id)
            serializer = RepresentationSerializer(repres)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @staticmethod
    @api_view(["POST"])
    def create(request):
        repre_service = RepresentationService()
        serializer = RepresentationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            repre = repre_service.create(
                serializer.validated_data,
                request.sign,
                request.user
            )
            return Response(
                {"representatation": str(repre)}, status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    