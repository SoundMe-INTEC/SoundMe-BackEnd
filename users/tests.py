from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from datetime import timedelta

from users.models import User
from users.services.user_services import UserService


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

	def test_check_returns_active_user_with_valid_credentials(self):
		user = self.create_user(is_active=True)

		authenticated_user = self.service.check(
			{"identification": user.identification, "password": "secure-password"}
		)

		self.assertEqual(authenticated_user, user)

	@patch.object(UserService, "_send_verification_email")
	def test_check_sends_otp_for_pending_user(self, send_email):
		user = self.create_user(is_active=False)

		checked_user = self.service.check(
			{"identification": user.identification, "password": "secure-password"}
		)

		user.refresh_from_db()
		self.assertEqual(checked_user, user)
		self.assertFalse(user.is_active)
		self.assertIsNotNone(user.otp_code)
		self.assertIsNotNone(user.otp_expires_at)
		send_email.assert_called_once_with(user)

	def test_check_activates_pending_user_with_valid_otp(self):
		user = self.create_user(
			is_active=False,
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
