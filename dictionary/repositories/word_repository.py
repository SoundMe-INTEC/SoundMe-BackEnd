from dictionary.models.word import Word
from dictionary.models.choices import Status

class WordRepository:
    
    def get_all(self):
        return Word.objects.all()
    
    def get_by_name(self, word_name):
        return Word.objects.filter(word_name=word_name).first()
    
    def get_by_id(self, word_id):
        return Word.objects.filter(id=word_id).first()
    
    def get_all_active(self):
        return Word.objects.filter(is_active=Status.ACTIVE)
    
    def create(self, new_word):
        new_word.save()
        return new_word
    
    def update(self, updated_word):
        updated_word.save()
        return updated_word
    
    def soft_delete(self, word_name):

        word = Word.objects.filter(word_name=word_name).first()
        
        if word is None:
            return False
        
        word.is_active = Status.INACTIVE
        word.save()
        
        return True
            
        
        
    
    