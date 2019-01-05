import mongoengine

ANIMAL_STATUS = ("SOLD", "DEAD", "ACTIVE", "REFERENCE")


class ReferenceAnimal(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField(required=True)
    ear_tag = mongoengine.StringField(required=False)
    birth_date = mongoengine.DateField(required=False)
    status = mongoengine.StringField(required=False, choices=ANIMAL_STATUS)

    meta = {
        "db_alias": "core",
        "collection": "reference_animal",
    }
