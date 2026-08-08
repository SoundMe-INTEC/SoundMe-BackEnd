from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.serializers import user_serializer
from users.services.user_services import UserService


class UserView:

    @staticmethod
    @api_view(["POST"])
    def signup(request):
        user_service = UserService()
        serializer = user_serializer.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_service.signup(serializer.validated_data)
            return Response(
                {"user": str(user.identification)}, status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    def login(request):
        user_service = UserService()
        serializer = user_serializer.LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_service.login(serializer.validated_data)
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "user": str(user.identification),
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    def reset_password(request):
        user_service = UserService()
        serializer = user_serializer.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = user_service.reset_password(serializer.validated_data)
            return Response({"message": str(result)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    def profile(request):
        user_service = UserService()
        identification = request.query_params.get("identification")
        if not identification:
            return Response(
                {"detail": "Identification query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = user_service.find_by_identification(identification)
            return Response(
                user_serializer.UserResponseSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    def search_users(request):
        user_service = UserService()
        try:
            users = user_service.find_all_active()
            serializer = user_serializer.UserResponseSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
