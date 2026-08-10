from rest_framework.decorators import api_view, permission_classes
from dictionary.services.sign_service import SignService
from dictionary.serializers.sign_serializer import SignSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class SignView():
    
    @staticmethod
    @api_view(["GET"])
    def get_all(request):
        sign_service = SignService()
        try:
            signs = sign_service.find_all_active()
            serializers = SignSerializer(signs, signs=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(["GET"])
    def get(request):
        sign_service = SignService()
        sign_name = request.query_params.get("sign_name")
        if not sign_name:
            return Response(    
                {"detail": "sign_name query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            sign = sign_service.find_by_sign_name(sign_name)
            serializer = SignSerializer(sign, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
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