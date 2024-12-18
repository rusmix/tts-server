# api/models.py

from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class RequestHistory(Document):
    text = StringField(required=True)
    file_name = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'request_history',
        'ordering': ['-timestamp']
    }
# api/models.py

from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class RequestHistory(Document):
    text = StringField(required=True)
    file_name = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'request_history',
        'ordering': ['-timestamp']
    }
