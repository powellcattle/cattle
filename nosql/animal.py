import mongoengine

from nosql.breed import Breed
from nosql.measurement import Measurement
from nosql.pasture import Pasture
from nosql.pregnancy_check import PregnancyCheck

ANIMAL_TYPES = ("COW", "CALF", "BULL")
ANIMAL_SEXES = ("HEIFER", "BULL", "STEER")
HORN_STATUS = ("POLLED", "DEHORNED", "SCURRED", "HORNED")
ANIMAL_STATUS = ("SOLD", "DEAD", "ACTIVE", "REFERENCE")
CONCEPTION_METHODS = ("NS", "ET", "AI")
EAR_TAG_COLORS = ("BLUE", "GREEN", "RED", "WHITE", "YELLOW", "PURPLE")
EAR_TAG_YEARS = (("A", 2013), ("B", 2014), ("C", 2015), ("D", 2016), ("E", 2017), ("F", 2018), ("G", 2019))


class Animal(mongoengine.Document):
    id = mongoengine.IntField(required=True, primary_key=True)
    ear_tag = mongoengine.StringField(required=False, null=False)
    ear_tag_loc = mongoengine.StringField(required=False)
    brand = mongoengine.StringField(required=False)
    brand_loc = mongoengine.StringField(required=False)
    other_id = mongoengine.StringField(required=False)
    electronic_id = mongoengine.StringField(required=False)
    animal_type = mongoengine.StringField(max_length=4, choices=ANIMAL_TYPES)
    sex = mongoengine.StringField(max_length=6, choices=ANIMAL_SEXES)

    horn_status = mongoengine.StringField(required=False, choices=HORN_STATUS)
    color_markings = mongoengine.StringField(required=False)
    status = mongoengine.StringField(required=False, choices=ANIMAL_STATUS)
    birth_date = mongoengine.DateField(required=False)
    yearling_date = mongoengine.DateField(required=False)
    conception_method = mongoengine.StringField(default="NS", choices=CONCEPTION_METHODS)
    purchased_date = mongoengine.DateField()
    purchased = mongoengine.BooleanField(default=False)
    # Reference fields
    breed = mongoengine.EmbeddedDocumentField(Breed)
    sire_animal = mongoengine.ReferenceField('self')
    dam_animal = mongoengine.ReferenceField('self')
    genetic_dam_animal = mongoengine.ReferenceField('self')
    real_dam_animal = mongoengine.ReferenceField('self')
    offspring = mongoengine.ListField(mongoengine.ReferenceField("self"))
    pasture = mongoengine.ReferenceField(Pasture)
    preg_checks = mongoengine.EmbeddedDocumentListField(PregnancyCheck)
    measurements = mongoengine.EmbeddedDocumentListField(Measurement)

    meta = {
        "db_alias": "core",
        'all_inheritance': True,
        "collection": "animal",
        "indexes": [
            {
                "fields": ["ear_tag"],
                "unique": False
            }
        ]
    }


