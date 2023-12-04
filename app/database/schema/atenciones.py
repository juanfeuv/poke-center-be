import datetime

from mongoengine import Document, StringField, DateTimeField, IntField, DictField

from app.core.config import settings
class Atenciones(Document):
    hp = IntField(required=True)
    trainerName = StringField(required=True)
    trainerId = StringField(required=True)
    cambioEstado = DictField(required=False, default={})
    nivel = IntField(required=True)
    pokemonName = StringField(required=True)
    createdAt = DateTimeField(default=datetime.datetime.now)
    pokemonId = IntField(required=True)
    pokemonInfo = DictField(required=False, default={})
    turnNumber = IntField(required=True)
    rawId = IntField(required=True)
    estado = StringField(required=False)
    comment = StringField(required=False)
    fechaAtencion = DateTimeField(required=False)
    user_id = StringField(required=True)
    meta = {
        "db_alias": settings.DB_ALIAS,
    }