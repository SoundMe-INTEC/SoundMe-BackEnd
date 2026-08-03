from repositories.sign_repositories import SignRepository
from dictionary.models import Sign

class SignService:
    
    def __init__(self):
        self._sign_repo = SignRepository()
        
    def create_sign(self, data):
        
        return self._user_repo.created(data)

    def find_by_sign_name(self, sign_name):
        
        sign = self._sign_repo.get_by_sign_name(sign_name)
        
        if sign is None:
            raise ValueError("Sign doesn't exist")
        
        return sign
    
    def find_all(self):
        
        return self._sign_repo.get_all()

    def find_all_active(self):
        
        return self._sign_repo.get_all_active()
    
    