from bson import json_util

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
        print(ear_tag)
        animal = Animal.objects(status="ACTIVE", ear_tag=ear_tag).first()
        if animal:
            calves = list()
            for offspring in animal.offspring:
                calf = dict()
                calf["ear_tag"] = str(offspring["ear_tag"])
                calf["status"] = str(offspring["status"])
                if offspring["birth_date"]:
                    calf["birth_date"] = offspring["birth_date"].strftime("%x")
                    print(calf["birth_date"])

                calves.append(calf)
            return jsonify(animal_details=calves)
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
