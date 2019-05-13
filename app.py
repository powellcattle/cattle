from animal import Animal

__author__ = 'spowell'
import logging
import datetime

from flask import Flask
from flask import request
from flask import render_template
from flask_jsonpify import jsonpify as jsonify
from nosql import mongo_setup

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s",
                    filename="flask_autocomplete.log",
                    filemode="w",
                    level=logging.DEBUG,
                    datefmt="%m/%d/%Y %I:%M:%S %p")

app = Flask(__name__)
flask_setup = {"host": "192.168.1.170", "port": "5000", "debug": False}


@app.before_first_request
def startup():
    mongo_setup.global_init()


@app.route("/cattle/_eartag_datails")
def eartag_details():
    try:
        ear_tag = request.args.get("get_eartag")
        found_animal = Animal.objects(status="ACTIVE", ear_tag=ear_tag).first()
        if found_animal:
            animal_list = list()
            for offspring in found_animal.offspring:
                animal_dict = dict()
                animal_dict["ear_tag"] = str(offspring["ear_tag"])
                animal_dict["status"] = str(offspring["status"])
                animal_dict["off_type"] = "CALF"
                if offspring["birth_date"]:
                    animal_dict["age"] = age(offspring["birth_date"])
                if offspring["sex"]:
                    if "STEER" == offspring["sex"]:
                        animal_dict["sex"] = "BULL"
                    else:
                        animal_dict["sex"] = offspring["sex"]
                else:
                    animal_dict["sex"] = "UNKNOWN"

                animal_list.append(animal_dict)

            return jsonify(animal_details=animal_list)
        else:
            return jsonify(animal_details="none")
    except Exception as e:
        return str(e)


def age(_date: datetime.date) -> int:
    today = datetime.date.today()
    delta = abs(today - _date)

    if int(delta.days / 365 * 12) < 12:
        return round(delta.days / 365 * 12)
    else:
        return round(delta.days / 365)


@app.route("/cattle/animal", methods=["GET"])
def get_animal():
    ear_tag = request.args.get("get_eartag")
    if ear_tag:
        animals = Animal.objects(status="ACTIVE", ear_tag__icontains=ear_tag)[:10]
    else:
        animals = Animal.objects(status="ACTIVE")[:5]
    results = list()
    if animals:
        for animal in animals:
            results.append(animal.to_mongo())
        return jsonify({"animals": results})
    else:
        return jsonify(results)


@app.route("/cattle/")
def render_animal():
    try:
        return render_template("test.html")
    except Exception as e:
        return (str(e))


if '__main__' == __name__:
    app.run(**flask_setup)
