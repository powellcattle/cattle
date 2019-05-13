import datetime

__author__ = 'spowell'











def age(_date: datetime.date) -> int:
    today = datetime.date.today()
    delta = abs(today - _date)

    if int(delta.days / 365 * 12) < 12:
        return round(delta.days / 365 * 12)
    else:
        return round(delta.days / 365)



dob = datetime.date(2018,1,20)
age = age(dob)
print(age)