from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.serializers import user_serializer
from users.services.user_services import EmailDeliveryError, UserService
from config.pagination import AdminResultsPagination


class UserView:

    @staticmethod
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def signup(request):
        user_service = UserService()
        serializer = user_serializer.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_service.signup(serializer.validated_data)
            return Response(
                {
                    "user": str(user.identification),
                    "message": "User created. Check your email for the OTP.",
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except EmailDeliveryError:
            return Response(
                {"message": "No se pudo enviar el código. Intenta de nuevo más tarde."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    @staticmethod
    @api_view(["POST"])
    @permission_classes([AllowAny])
    def check(request):
        user_service = UserService()
        serializer = user_serializer.CheckCredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_service.check(serializer.validated_data)
            return Response(
                {
                    "user": str(user.identification),
                    "requires_otp": not user.is_active,
                    "message": "OTP sent to your email." if not user.is_active else "Credentials verified.",
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except EmailDeliveryError:
            return Response(
                {"message": "No se pudo enviar el código. Intenta de nuevo más tarde."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    @staticmethod
    @api_view(["POST"])
    @permission_classes([AllowAny])
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
    @permission_classes([AllowAny])
    def verify_otp(request):
        user_service = UserService()
        serializer = user_serializer.VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_service.verify_otp(serializer.validated_data)
            return Response(
                {
                    "user": str(user.identification),
                    "message": "OTP verified successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def reset_password(request):
        user_service = UserService()
        serializer = user_serializer.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        requested_identification = serializer.validated_data["identification"]
        if requested_identification != request.user.identification and not request.user.is_staff:
            return Response(
                {"detail": "You can only reset your own password."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            result = user_service.reset_password(serializer.validated_data)
            return Response({"message": str(result)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([IsAuthenticated])
    def profile(request):
        user_service = UserService()
        identification = request.query_params.get("identification") or request.user.identification

        if identification != request.user.identification and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to view this profile."},
                status=status.HTTP_403_FORBIDDEN,
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
    @permission_classes([IsAuthenticated])
    def search_users(request):
        user_service = UserService()
        try:
            users = user_service.find_all_active()
            serializer = user_serializer.UserResponseSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["GET"])
    @permission_classes([IsAdminUser])
    def list_admin(request):
        user_service = UserService()
        users = user_service.find_all().order_by("identification")

        search = request.query_params.get("search")
        if search:
            users = users.filter(identification__icontains=search)

        paginator = AdminResultsPagination()
        page = paginator.paginate_queryset(users, request)
        serializer = user_serializer.UserResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def admin_create_user(request):
        user_service = UserService()
        serializer = user_serializer.AdminCreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_service.admin_create(serializer.validated_data)
            return Response(
                user_serializer.UserResponseSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["PATCH"])
    @permission_classes([IsAdminUser])
    def update_user(request):
        user_service = UserService()
        serializer = user_serializer.UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = user_service.update(serializer.validated_data)
            return Response(
                user_serializer.UserResponseSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def deactivate_user(request):
        user_service = UserService()
        identification = request.data.get("identification")
        if not identification:
            return Response(
                {"detail": "identification is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = user_service.deactivate(identification)
            return Response(
                user_serializer.UserResponseSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAdminUser])
    def activate_user(request):
        user_service = UserService()
        identification = request.data.get("identification")
        if not identification:
            return Response(
                {"detail": "identification is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = user_service.activate(identification)
            return Response(
                user_serializer.UserResponseSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
