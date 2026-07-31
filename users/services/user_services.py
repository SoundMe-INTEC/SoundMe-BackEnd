from repositories.user_repository import UserRepository
from users.models import User

class UserService():

    def __init__(self):
        self.repository = UserRepository()

    def create(self, data):

        user_repo = self.repository

        if user_repo.get_by_identification(data["identification"]):
            raise ValueError("User already exists")
        
        user = User(
            identification = data["identification"],
            identification_type= data["identification_type"],
            email = data["email"],
            password = data["password"]
        )

        return user_repo.create(user)