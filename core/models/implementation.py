from django.utils import timezone
from .abstration import TempCode as AbstractTempCode 
from .abstration import Users as AbstractUsers
from .abstration import Category as AbstractCategory
from .abstration import Product as AbstractProduct





class TempCode(AbstractTempCode):
    
    def save(self, request, *args, **kwargs):
        from datetime import timedelta
        
        self.expires = timezone.now() + timedelta(minutes=10)
        
        super().save(*args, **kwargs)
        
    @classmethod
    
    def get_string_code(cls, code_type: str):
        if code_type == "signup":
            return "12345"
        else:
            return "ab243d-ef1452" 
        
        
class Users(AbstractUsers):
    pass        

class Category(AbstractCategory):
    pass

class Product(AbstractProduct):
    pass