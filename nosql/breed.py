import mongoengine

Breeds = ({"name": "ANGUS", "gestation": 285},
          {"name": "BRAHMAN", "gestation": 285},
          {"name": "BRANGUS", "gestation": 285},
          {"name": "CHAROLAIS", "gestation": 289},
          {"name": "HERFORD", "gestation": 285},
          {"name": "BRANGUS F1", "gestation": 285},
          {"name": "COMMERCIAL", "gestation": 285},
          {"name": "BRAFORD", "gestation": 285},
          {"name": "CHARBRAY", "gestation": 285})


class Breed(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=True)
    gestation_period = mongoengine.IntField(required=True)


class BreedTemp(mongoengine.Document):
    id = mongoengine.IntField(required=True, primary_key=True)
    name = mongoengine.StringField(required=True)
    gestation_period = mongoengine.IntField(required=True)

    meta = {
        "db_alias": "core",
        "collection": "breed_temp",
    }
