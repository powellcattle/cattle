from animal import Animal

__author__ = 'spowell'
import logging

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
flask_setup = {"host": "192.168.1.170", "port": "5000", "debug": True}


@app.before_first_request
def startup():
    mongo_setup.global_init()

@app.route("/_eartag_datails")
def eartag_details():
    try:
        ear_tag = request.args.get("eartag")
        found_animal = Animal.objects(status="ACTIVE", ear_tag=ear_tag).first()
        if found_animal:
            animal_list = list()

            if found_animal.sire_animal:
                animal_dict = dict()
                animal_dict["ear_tag"] = found_animal.sire_animal.ear_tag
                animal_dict["off_type"] = "SIRE"
                animal_list.append(animal_dict)
            if found_animal.dam_animal:
                animal_dict = dict()
                animal_dict["ear_tag"] = found_animal.dam_animal.ear_tag
                animal_dict["off_type"] = "DAM"
                animal_list.append(animal_dict)

            for offspring in found_animal.offspring:
                animal_dict = dict()
                animal_dict["ear_tag"] = str(offspring["ear_tag"])
                animal_dict["status"] = str(offspring["status"])
                animal_dict["off_type"] = "CALF"
                if offspring["birth_date"]:
                    animal_dict["birth_date"] = offspring["birth_date"].strftime("%x")

                animal_list.append(animal_dict)
            return jsonify(animal_details=animal_list)
        else:
            return jsonify(animal_details="none")
    except Exception as e:
        return(str(e))


@app.route("/animal", methods=["GET"])
def get_animal():

    ear_tag = request.args.get("ear_tag")
    if ear_tag:
        animals = Animal.objects(status="ACTIVE", ear_tag__icontains=ear_tag)[:5]
    else:
        animals = Animal.objects(status="ACTIVE")[:5]
    results = list()
    if animals:

        for animal in animals:
            results.append(animal.to_mongo())
        return jsonify({"animals": results})
    else:
        return jsonify(results)

@app.route("/home/")
def animal():
    try:
        return render_template("animal.html")
    except Exception as e:
        return(str(e))


if '__main__' == __name__:
    app.run(**flask_setup)
