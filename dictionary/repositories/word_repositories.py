from dictionary.models import Word

class WordRepository:
    
    def get_all(self):
        return Word.objects.filter(is_active=True)
    
    def get_by_name(self, word_name):
        return Word.objects.filter(word_name=word_name).first
    
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
        
        word.is_active = False
        word.save()
        
        return True
            
        
        
    
    