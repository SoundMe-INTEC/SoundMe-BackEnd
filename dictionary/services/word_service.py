from dictionary.repositories.word_repository import WordRepository
from dictionary.models.word import Word

class WordService:
    
    def __init__(self):
        self._word_repo = WordRepository()
    
    def create(self, data, user):
        
        word = Word(
            created_by=user,
            word_name=data["word_name"],
            grammatical_category=data["grammatical_category"],
            description=data["description"]
        )
        return self._word_repo.create(word)
    
    def find_by_word_name(self, word_name):
        
        word = self._word_repo.get_by_name(word_name)
        
        if word is None: 
            raise ValueError("Word doesn't exist")
        
        return word
    
    def find_all(self):
        
        return self._word_repo.get_all()
    
    def find_all_active(self):
        
        return self._word_repo.get_all_active()
        
    def update(self, word_name, data):
        
        word = self.find_by_word_name(word_name)     
           
        new_name = data.get("word_name")
        
        if new_name and new_name != word.word_name:
            word.word_name = new_name
            
        new_description = data.get("description")
        
        if new_description and new_description != word.description:
            word.description = new_description
            
        new_category = data.get("grammatical_category")
        
        if new_category and new_category != word.grammatical_category:
            word.grammatical_category = new_category
        
        allowed_to_change = ("word_name", "description", "grammatical_category")
        
        for field in allowed_to_change:
            if field in data: 
                setattr(word, field, data[field])
        
        return self._word_repo.update(word)
        
    def soft_delete(self, word_name):
        
        is_deleted = self._word_repo.soft_delete(word_name)
        
        return(
            f"word : {word_name} has been deleted"
            if is_deleted
            else "word could not be found"
        )