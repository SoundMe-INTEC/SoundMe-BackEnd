from users.models import User
from django.db.models import QuerySet


class UserRepository:

    def get_by_identification(self, identification: str) -> User | None:
        return User.objects.filter(identification=identification).first()

    def get_by_email(self, email: str) -> User | None:
        return User.objects.filter(email=email).first()

    def get_all(self) -> QuerySet[User]:
        return User.objects.all()

    def get_all_active(self) -> QuerySet[User]:
        return User.objects.filter(is_active=True)

    def create(self, new_user: User) -> User:
        new_user.save()
        return new_user

    def update(self, updated_user: User) -> User:
        updated_user.save()
        return updated_user

    def soft_delete(self, identification: str) -> bool:

        user = User.objects.filter(identification=identification).first()

        if user is None:
            return False

        user.is_active = False
        user.save()

        return True
