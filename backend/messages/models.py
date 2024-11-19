from django.db import models

# Create your models here.
'''
CLASS: Message
'''
class Message:
    # We cant use django model stuff due to our custom db implementation
    # message_text = models.TextField()

    #Constructor
    def __init__(self, message_id, sender_id, receiver_id, content):
        self.message_id = message_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
    
    #Getters
    def get_message_id(self):
        return self.message_id
    def get_content(self):
        return self.content
    def get_sender_id(self):
        return self.sender_id
    def get_receiver_id(self):
        return self.receiver_id
    

