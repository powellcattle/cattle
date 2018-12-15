import mongoengine


class Pasture(mongoengine.Document):
    id = mongoengine.IntField(required=True, primary_key=True)
    name = mongoengine.StringField(required=True)
    premise_id = mongoengine.StringField()
    acres = mongoengine.FloatField()

    meta = {
        "db_alias": "core",
        "collection": "pasture",
    }
