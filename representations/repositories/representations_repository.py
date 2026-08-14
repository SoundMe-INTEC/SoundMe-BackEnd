from representations.models.representation import Representation

class RepresentationRepository:
    def get_all_active(self):
        return Representation.objects.filter(is_active=True)
    
    def get_by_id(self, sign_id):
        return Representation.objects.filter(sign_id=sign_id).first() 
    
    def create(self, new_representation):
        new_representation.save()
        return new_representation
    
    def update(self, updated_representation):
        updated_representation.saave()
        return updated_representation
    
    def soft_delete(self, sign_id):
        
        representation = self.get_by_id(sign_id=sign_id)
        
        if representation is None:
            return False
        
        representation.is_active = False
        representation.save()
        
        return True