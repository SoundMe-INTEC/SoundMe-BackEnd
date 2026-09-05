from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch
import requests
from rest_framework.test import APIRequestFactory

from datetime import timedelta

from users.api.user_view import UserView
from users.models import User
from users.services.user_services import EmailDeliveryError, UserService


class UserServiceCheckTests(TestCase):
	def setUp(self):
		self.service = UserService()

	def create_user(self, *, is_active, otp_code=None, otp_expires_at=None):
		user = User(
			identification="001-0000000-1",
			identification_type="IDCard",
			email="user@example.com",
			is_active=is_active,
			otp_code=otp_code,
			otp_expires_at=otp_expires_at,
		)
		user.set_password("secure-password")
		user.save()
		return user

	@patch.object(UserService, "_send_verification_email")
	def test_check_sends_otp_for_active_user(self, send_email):
		user = self.create_user(is_active=True)

		checked_user = self.service.check(
			{"identification": user.identification, "password": "secure-password"}
		)

		user.refresh_from_db()
		self.assertEqual(checked_user, user)
		self.assertIsNotNone(user.otp_code)
		self.assertIsNotNone(user.otp_expires_at)
		send_email.assert_called_once_with(user)

	def test_check_rejects_disabled_user(self):
		user = self.create_user(is_active=False)

		with self.assertRaisesMessage(ValueError, "User account is disabled"):
			self.service.check(
				{"identification": user.identification, "password": "secure-password"}
			)

	@patch(
		"users.services.user_services.requests.post",
		side_effect=requests.exceptions.ConnectTimeout,
	)
	def test_check_raises_delivery_error_when_smtp_times_out(self, mock_post):
		user = self.create_user(is_active=True)

		with self.assertRaises(EmailDeliveryError):
			self.service.check(
				{"identification": user.identification, "password": "secure-password"}
			)

	def test_login_succeeds_without_otp_temporarily(self):
		user = self.create_user(is_active=True)

		authenticated_user = self.service.login(
			{"identification": user.identification, "password": "secure-password"}
		)

		self.assertEqual(authenticated_user, user)

	def test_login_succeeds_with_valid_otp(self):
		user = self.create_user(
			is_active=True,
			otp_code="123456",
			otp_expires_at=timezone.now() + timedelta(minutes=10),
		)

		authenticated_user = self.service.login(
			{
				"identification": user.identification,
				"password": "secure-password",
				"otp": "123456",
			}
		)

		user.refresh_from_db()
		self.assertEqual(authenticated_user, user)
		self.assertTrue(user.is_active)
		self.assertIsNone(user.otp_code)
		self.assertIsNone(user.otp_expires_at)

	def test_login_rejects_disabled_user(self):
		user = self.create_user(
			is_active=False,
			otp_code="123456",
			otp_expires_at=timezone.now() + timedelta(minutes=10),
		)

		with self.assertRaisesMessage(ValueError, "User account is disabled"):
			self.service.login(
				{
					"identification": user.identification,
					"password": "secure-password",
					"otp": "123456",
				}
			)

	@patch.object(UserService, "check", side_effect=EmailDeliveryError)
	def test_check_endpoint_returns_503_when_email_delivery_fails(self, check):
		request = APIRequestFactory().post(
			"/api/check",
			{"identification": "001-0000000-1", "password": "secure-password"},
			format="json",
		)

		response = UserView.check(request)

		self.assertEqual(response.status_code, 503)
		self.assertEqual(response.data["message"], "No se pudo enviar el código. Intenta de nuevo más tarde.")
