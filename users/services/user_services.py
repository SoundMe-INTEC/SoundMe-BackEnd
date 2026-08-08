from repositories.user_repository import UserRepository
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

        return self._user_repo.create(user)

    def login(self, data):

        user = self._user_repo.get_by_identification(data["identification"])

        if user is None or not user.check_password(data["password"]):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User account is disabled")

        return user

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
