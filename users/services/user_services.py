import secrets
from datetime import timedelta
from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from users.repositories.user_repository import UserRepository
from users.models import User


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

        user.set_password(data["password"])
        user.is_active = False
        return self._user_repo.create(user)

    def _send_verification_email(self, user):
        subject = "Tu código de verificación de SoundMe"
        text_body = (
            "Tu código de verificación de SoundMe es: "
            f"{user.otp_code}. Vence en 10 minutos."
        )
        html_body = render_to_string(
            "users/emails/otp_verification.html",
            {"otp_code": user.otp_code},
        )
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_body, "text/html")

        logo_path = settings.BASE_DIR / "users/static/users/images/soundme_logo.png"
        with logo_path.open("rb") as logo_file:
            logo = MIMEImage(logo_file.read())
        logo.add_header("Content-ID", "<soundme-logo>")
        logo.add_header("Content-Disposition", "inline", filename="soundme_logo.png")
        email.attach(logo)
        email.send(fail_silently=False)

    def verify_otp(self, data):
        user = self.find_by_identification(data["identification"])

        if user.is_active:
            raise ValueError("User is already verified")

        self._activate_with_otp(user, data["otp"])
        return user

    def check(self, data):
        user = self._user_repo.get_by_identification(data["identification"])

        if user is None or not user.check_password(data["password"]):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            user.otp_code = f"{secrets.randbelow(1_000_000):06d}"
            user.otp_expires_at = timezone.now() + timedelta(minutes=10)
            self._user_repo.update(user)
            self._send_verification_email(user)

        return user

    def login(self, data):
        user = self._user_repo.get_by_identification(data["identification"])

        if user is None or not user.check_password(data["password"]):
            raise ValueError("Invalid credentials")

        if user.is_active:
            return user

        otp = data.get("otp")
        if not otp:
            raise ValueError("OTP verification required")

        self._activate_with_otp(user, otp)
        return user

    def _activate_with_otp(self, user, otp):
        if (
            not user.otp_code
            or user.otp_code != otp
            or not user.otp_expires_at
            or timezone.now() >= user.otp_expires_at
        ):
            raise ValueError("Invalid or expired OTP")

        user.is_active = True
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

        allowed_to_change = ("identification_type", "phone", "role")

        for field in allowed_to_change:
            if field in data:
                setattr(user, field, data[field])

        return self._user_repo.update(user)

    def soft_delete(self, identification):

        is_deleted = self._user_repo.soft_delete(identification)

        return (
            f" User: {identification} has been deleted"
            if is_deleted
            else "User could not be deleted"
        )
