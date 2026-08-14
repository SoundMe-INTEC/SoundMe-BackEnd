from dictionary.repositories.sign_repository import SignRepository
from dictionary.models.sign import Sign

class SignService:
    
    def __init__(self):
        self._sign_repo = SignRepository()
        
    def create(self, data, user):
        
        sign = Sign(
            created_by=user,
            sign_name=data["sign_name"],
            sign_category=data["sign_category"],
            description=data["description"]
        )
        
        return self._sign_repo.create(sign)

    def find_by_sign_name(self, sign_name):
        
        sign = self._sign_repo.get_by_name(sign_name)
        
        if sign is None:
            raise ValueError("Sign doesn't exist")
        
        return sign
    
    def find_all(self):
        
        return self._sign_repo.get_all()

    def find_all_active(self):
        
        return self._sign_repo.get_all_active()
    
    def update(self, sign_name, data):
        
        sign = self.find_by_sign_name(sign_name)
        
        new_name = data.get("sign_name")
        
        if new_name and new_name != sign.sign_name:
            sign.sign_name = new_name
            
        new_description = data.get("description")
        
        if new_description and new_description != sign.description:
            sign.description = new_description
            
        new_category = data.get("sign_category")
        
        if new_category and new_category != sign.sign_category:
            sign.sign_category = new_category
        
        allowed_to_change = ("sign_name", "description", "sign_category")
        
        for field in allowed_to_change:
            if field in data: 
                setattr(sign, field, data[field])
        
        return self._sign_repo.update(sign)
        
    def soft_delete(self, sign_name):
        
        is_deleted = self._sign_repo.soft_delete(sign_name)
        
        return(
            f"sign : {sign_name} has been deleted"
            if is_deleted
            else "Sign could not be found"
        )