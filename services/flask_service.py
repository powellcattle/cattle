import mongoengine
from bson import json_util

from nosql.animal import Animal

__author__ = 'spowell'
import logging

from flask import Flask
from flask import request

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s",
                    filename="flask_autocomplete.log",
                    filemode="w",
                    level=logging.DEBUG,
                    datefmt="%m/%d/%Y %I:%M:%S %p")

app = Flask(__name__)

list_streets = list()
list_addresses = list()

def global_init():
    mongoengine.register_connection(alias="core", name="cattle",host="192.168.1.130")

@app.before_first_request
def startup():
    global_init()
    print("startup")
    # global list_streets
    # global list_addresses
    # list_streets = ec_psql_util.sql_get_streets()
    # list_addresses = ec_psql_util.sql_get_addresses()


@app.route("/animal", methods=["GET"])
def get_streets():
    global list_streets
    list_candidates = list()

    req = request.args.get("req").upper()

    animals = Animal.objects(ear_tag__icontains=req)

    for animal in animals:
        print(animal.ear_tag)

    return json_util.default(animals)


# @app.route("/addresses", methods=["GET"])
# def get_addresses():
#     global list_addresses
#
#     list_candidates = list()
#
#     req = request.args.get("req").upper()
#
#     for value in list_addresses:
#         if req in value["address"]:
#             list_candidates.append(value)
#             # if list_candidates.__len__() >= 10:
#             #     break
#
#     return jsonify(list_candidates)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
