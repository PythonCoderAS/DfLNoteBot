from os.path import abspath, join

from tortoise import Tortoise
from tortoise.fields import BigIntField, BooleanField, CharField, IntField
from tortoise.models import Model

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://" + abspath(join(__file__, "..", "..", "db.sqlite3"))
    },
    "apps": {
        "orm": {
            "models": ["src.orm"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "maxsize": 20,
}


class Note(Model):
    id = IntField(pk=True)
    channel_id = BigIntField(null=False)
    text = CharField(max_length=4096, null=False)
    image_url = CharField(max_length=256, null=True, default=None)
    resolved = BooleanField(null=False, default=False)

    chapter = CharField(max_length=256, null=True, default=None)
    page = CharField(max_length=256, null=True, default=None)
    panel = CharField(max_length=256, null=True, default=None)
    bubble = CharField(max_length=256, null=True, default=None)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"<Note id={self.id} channel_id={self.channel_id} text={self.text} resolved={self.resolved}>"


async def init():
    """Initialize the ORM."""
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas()
