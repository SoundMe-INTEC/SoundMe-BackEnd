from repositories.word_repositories import WordRepository
from dictionary.models import Word

class WordService:
    
    def __init__(self):
        self._word_repo = WordRepository()
    
    def create_word(self, data):
        
        return self._word_repo.create(data)
    
    def find_by_word_name(self, word_name):
        
        word = self._word_repo.get_by_name(word_name)
        
        if word is None: 
            raise ValueError("Word doesn't exist")
        
        return word
        