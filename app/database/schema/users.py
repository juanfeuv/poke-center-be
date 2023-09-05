import datetime

from mongoengine import Document, StringField, DateTimeField

from app.core.config import settings
class Users(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    status = StringField(required=True, default="active")
    createdBy = StringField(required=True)
    modifiedBy = StringField(required=True)
    createdDate = DateTimeField(default=datetime.datetime.now)
    modifiedDate = DateTimeField(default=datetime.datetime.now)
    meta = {
        "db_alias": settings.DB_ALIAS,
    }