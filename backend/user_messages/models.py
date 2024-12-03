# Create your models here.
'''
CLASS: Message
'''
class Message:
    # We cant use django model stuff due to our custom db implementation
    # message_text = models.TextField()

    #Constructor
    def __init__(self, id, sender, receiver, content):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.content = content
    

