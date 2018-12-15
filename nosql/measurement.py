import mongoengine


class Measurement(mongoengine.EmbeddedDocument):
    MEASUREMENT_CATEGORY = ("BIRTH", "WEANING", "YEARLING", "GAIN", "WORKING WEIGHT")
    category = mongoengine.StringField(required=True, choices=MEASUREMENT_CATEGORY)
    measure_date = mongoengine.DateField(required=True)
    age_at_measure = mongoengine.IntField()
    weight = mongoengine.IntField()
    adjusted_weight = mongoengine.IntField()
    adg = mongoengine.FloatField()
    wda = mongoengine.FloatField()
    scrotal = mongoengine.FloatField()
    reference_date = mongoengine.DateField()
    reference_weight = mongoengine.IntField()
    gain = mongoengine.IntField()
    comments = mongoengine.StringField()
