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
    # We might need to make our own abstract user
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
    def __init__(self, id, title, description, price, image, author_id, tags, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.image = image
        self.author_id = author_id
        self.tags = tags
        self.created_at = created_at

    def __str__(self):
        return self.title
    


