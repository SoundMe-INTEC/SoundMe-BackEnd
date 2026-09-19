import secrets
from datetime import timedelta

import requests
from django.conf import settings
from django.utils import timezone

from users.repositories.user_repository import UserRepository
from users.models import User


class EmailDeliveryError(Exception):
    pass


class UserService:

    def __init__(self):
        self._user_repo = UserRepository()

    def signup(self, data):

        if self._user_repo.get_by_identification(data["identification"]):
            raise ValueError("User with this identification already exists")

        if self._user_repo.get_by_email(data["email"]):
            raise ValueError("User with this email already exists")

        user = User(
            identification=data["identification"],
            identification_type=data["identification_type"],
            email=data["email"],
        )

        # El usuario queda habilitado desde el registro; el OTP obligatorio en
        # el primer login confirma la propiedad del correo.
        user.set_password(data["password"])
        return self._user_repo.create(user)

    def _send_verification_email(self, user):
        if not settings.MAIL_RELAY_URL or not settings.MAIL_RELAY_API_KEY:
            raise EmailDeliveryError("MAIL_RELAY_URL and MAIL_RELAY_API_KEY must be configured")

        try:
            response = requests.post(
                f"{settings.MAIL_RELAY_URL.rstrip('/')}/send-otp-email",
                json={"to_email": user.email, "otp_code": user.otp_code},
                headers={"X-API-Key": settings.MAIL_RELAY_API_KEY},
                timeout=settings.MAIL_RELAY_TIMEOUT,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise EmailDeliveryError("Unable to send OTP email") from error

    def verify_otp(self, data):
        user = self.find_by_identification(data["identification"])
        self._consume_otp(user, data["otp"])
        return user

    def check(self, data):
        user = self._user_repo.get_by_identification(data["identification"])

        if user is None or not user.check_password(data["password"]):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User account is disabled")

        # Se solicita OTP a todos los usuarios en cada inicio de sesión, no solo
        # en la primera verificación de cuenta.
        user.otp_code = f"{secrets.randbelow(1_000_000):06d}"
        user.otp_expires_at = timezone.now() + timedelta(minutes=10)
        self._user_repo.update(user)
        self._send_verification_email(user)

        return user

    def login(self, data):
        user = self._user_repo.get_by_identification(data["identification"])

        if user is None or not user.check_password(data["password"]):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User account is disabled")

        otp = data.get("otp")
        if otp:
            self._consume_otp(user, otp)

        return user

    def _consume_otp(self, user, otp):
        if (
            not user.otp_code
            or user.otp_code != otp
            or not user.otp_expires_at
            or timezone.now() >= user.otp_expires_at
        ):
            raise ValueError("Invalid or expired OTP")

        user.otp_code = None
        user.otp_expires_at = None
        self._user_repo.update(user)

    def reset_password(self, data):

        user = self.find_by_identification(data["identification"])

        user.set_password(data["new_password"])
        self._user_repo.update(user)

        return f"Password of user {data['identification']} has been changed"

    def find_by_identification(self, identification):

        user = self._user_repo.get_by_identification(identification)

        if user is None:
            raise ValueError("User doesn't exist")

        return user

    def find_by_email(self, email):

        user = self._user_repo.get_by_email(email)

        if user is None:
            raise ValueError("User doesn't exist")

        return user

    def find_all(self):

        return self._user_repo.get_all()

    def find_all_active(self):

        return self._user_repo.get_all_active()

    def update(self, data):

        user = self.find_by_identification(data["identification"])

        new_email = data.get("email")   

        if new_email and new_email != user.email:
            existing_user = self._user_repo.get_by_email(new_email)
            if existing_user:
                raise ValueError("Email is already in use by another user")
            user.email = new_email

        new_identification = data.get("identification")

        if new_identification and new_identification != user.identification:
            existing_user = self._user_repo.get_by_identification(new_identification)
            if existing_user:
                raise ValueError("Identification is already in use by another user")
            user.identification = new_identification

        allowed_to_change = ("identification_type", "phone", "role", "is_staff")

        for field in allowed_to_change:
            if field in data:
                setattr(user, field, data[field])

        return self._user_repo.update(user)

    def admin_create(self, data):

        if self._user_repo.get_by_identification(data["identification"]):
            raise ValueError("User with this identification already exists")

        if self._user_repo.get_by_email(data["email"]):
            raise ValueError("User with this email already exists")

        user = User(
            identification=data["identification"],
            identification_type=data["identification_type"],
            email=data["email"],
            phone=data.get("phone") or None,
            is_staff=data.get("is_staff", False),
            is_active=True,
        )

        user.set_password(data["password"])
        return self._user_repo.create(user)

    def deactivate(self, identification):

        is_deactivated = self._user_repo.soft_delete(identification)

        if not is_deactivated:
            raise ValueError("User doesn't exist")

        return self.find_by_identification(identification)

    def activate(self, identification):

        is_activated = self._user_repo.reactivate(identification)

        if not is_activated:
            raise ValueError("User doesn't exist")

        return self.find_by_identification(identification)

    def soft_delete(self, identification):

        is_deleted = self._user_repo.soft_delete(identification)

        return (
            f" User: {identification} has been deleted"
            if is_deleted
            else "User could not be deleted"
        )
