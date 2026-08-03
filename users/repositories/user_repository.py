from users.models import User
from django.db.models import QuerySet


class UserRepository:

    def get_by_identification(self, identification):
        return User.objects.filter(identification=identification).first()

    def get_by_email(self, email):
        return User.objects.filter(email=email).first()

    def get_all(self):
        return User.objects.all()

    def get_all_active(self):
        return User.objects.filter(is_active=True)
    
    def create(self, new_user):
        new_user.save()
        return new_user

    def update(self, updated_user):
        updated_user.save()
        return updated_user
    
    def soft_delete(self, identification):

        user = User.objects.filter(identification=identification).first()

        if user is None:
            return False

        user.is_active = False
        user.save()

        return True
