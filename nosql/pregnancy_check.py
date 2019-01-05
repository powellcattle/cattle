import mongoengine

PREG_CHECK_METHOD = ("PALPATION", "BLOOD", "ULTRASOUND", "OBSERVATION")
PREG_CHECK_RESULT = ("PREGNANT", "OPEN", "RECHECK")


class PregnancyCheck(mongoengine.EmbeddedDocument):
    id = mongoengine.IntField(required=True, primary_key=True)
    animal_id = mongoengine.IntField()
    check_date = mongoengine.DateField()
    check_method = mongoengine.StringField(required=True, choices=PREG_CHECK_METHOD)
    result = mongoengine.StringField(required=True, choices=PREG_CHECK_RESULT)
    time_pregnant = mongoengine.IntField()
    expected_due_date = mongoengine.DateField()
    comments = mongoengine.StringField()
