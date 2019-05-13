import mongoengine


class Treatment(mongoengine.EmbeddedDocument):
    treatment_date = mongoengine.DateField(required=True)
    category = mongoengine.StringField()
    medication = mongoengine.StringField()
    dosage = mongoengine.StringField()
