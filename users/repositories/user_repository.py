from users.models import User
from django.db.models import QuerySet

def get_by_identification (self, identification: str) -> User | None:
    try:
        return User.objects.get(identification=identification)
    except User.DoesNotExist:
        return None
    
def get_by_email (self, email:str) -> User | None:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def get_all (self) -> QuerySet[User]:
    return User.objects.all()

def get_all_active (self) -> QuerySet[User]:
    return User.objects.filter(is_active=True)

def create (self, new_user: User) -> User:
    new_user.save()
    return new_user

def update (self, updated_user: User) -> User:
    updated_user.save()
    return updated_user

def soft_delete (self, identification) -> bool:

    user = User.objects.get(identification=identification)

    if user == None:
        return False

    user.is_active = False
    user.save()
    return True