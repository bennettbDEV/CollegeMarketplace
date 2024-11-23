from django.contrib.auth.hashers import check_password
'''
CONTAINS:
-Classes: User, Message, SMS Message, Listing

'''

# Create your models here. Models are essentially DB tables
'''
CLASS: User
'''
class User:
    #Functions
    def __init__(self, id, username, password=None, location=None):
        self.id = id
        self.username = username
        self.password = password  # Store hashed password directly
        self.location = location
        
    def __str__(self):
        return self.username   
    
    @property
    def is_authenticated(self):
        return True
    
    def check_password(self, password):
        return check_password(password, self.password) 
    

'''
CLASS: Message
'''
class Message:
    # We cant use django model stuff due to our custom db implementation
    # message_text = models.TextField()

    #Functions
    def __init__(self, id):
        self.id = id

'''
SUB-CLASS: SMS Message
'''
class SMSMessage(Message):
    # SMS-specific fields
    # Functions        
    def __init__(self, id):
        self.id = id

'''
CLASS: Listing
'''
class Listing:
    def __init__(self, id, title, condition, description, price, image, likes, dislikes, tags, created_at, author_id):
        self.id = id
        self.title = title
        self.condition = condition
        self.description = description
        self.price = price
        self.image = image
        self.likes = likes
        self.dislikes = dislikes
        self.tags = tags
        self.author_id = author_id
        self.created_at = created_at

    def __str__(self):
        return self.title
    


