from repositories.representations_repository import RepresentationRepository
from representations.models.representation import Representation


class RepresentationService:
    
    def __init__(self):
        self._repre_repo = RepresentationRepository()
        
    def find_all_active(self):
        return self._repre_repo.get_all_active()
    
    def find_by_id(self, sign_id):
    
        repre = self._repre_repo.get_by_id(sign_id)
        
        if repre is None:
            raise ValueError("Repre doesn't exist")
        
        return repre
    
    def create(self, data, user, sign):
        
        repre = Representation(
            sign_id=sign,
            created_by=user,
            extension=data["extension"],
            url=data["url"]
        )
        
        return self._repre_repo.create(repre)
    
    def update(self, sign_id, data):
        
        repre = self._repre_repo.get_by_id(sign_id)
        
        new_url = data.get("url")
        
        if new_url and new_url != repre.url:
            repre.url = new_url 
        
        new_extension = data.get("extension")
        
        if new_extension and new_extension != repre.extension:
            repre.extension = new_extension
        
        allowed_to_change = ("url", "extension")  
        
        for field in allowed_to_change:
            if field in data:
                setattr(repre, field, data[field])     
        
        return self._repre_repo.update(repre)
    
    def soft_delte(self, sign_id):
        
        is_delete = self._repre_repo.soft_delete(sign_id)
        
        return(
            f"repre: {sign_id} has been deleted"
            if is_delete
            else "Representation could not be found"
        )  
           
        
            
        