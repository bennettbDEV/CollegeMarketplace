# Create your models here.
"""
CLASS: Message
"""

class Message:
    # We cant use django model stuff due to our custom db implementation
    # message_text = models.TextField()

    # Constructor
    def __init__(self, id, sender_id, receiver_id, content):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content