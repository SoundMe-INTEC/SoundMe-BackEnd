from dictionary.models import Sign

class SignRepository:
    
    def get_by_sign_name(self, sign_name):
        return Sign.objects.filter(sign_name=sign_name).first()
    
    def get_all(self):
        return Sign.objects.all()
    
    def get_all_active(self):
        return Sign.objects.filter(is_active=True)
    
    def create(self, new_sign):
        new_sign.save()
        return new_sign
    
    def update(self, updated_sign):
        updated_sign.save()
        return updated_sign
    
    def soft_delete(self, sign_name):
        
        sign = Sign.objects.filter(sign_name=sign_name).first()
        
        if sign is None:
            return False
        
        sign.is_active = False
        sign.save()
        
        return True
    
    
        