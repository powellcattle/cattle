from typing import List, Any

__author__ = 'spowell'
import logging

from flask import Flask
from flask import request
from nosql import mongo_setup
from flask_jsonpify import jsonpify as jsonify

import ec_psql_util

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s",
                    filename="flask_autocomplete.log",
                    filemode="w",
                    level=logging.DEBUG,
                    datefmt="%m/%d/%Y %I:%M:%S %p")

app = Flask(__name__)

list_streets = list()
list_addresses = list()


@app.before_first_request
def startup():
    mongo_setup()
    # global list_streets
    # global list_addresses
    # list_streets = ec_psql_util.sql_get_streets()
    # list_addresses = ec_psql_util.sql_get_addresses()


@app.route("/streets", methods=["GET"])
def get_streets():
    global list_streets
    list_candidates = list()

    req = request.args.get("req").upper()

    for value in list_streets:
        if req in value["street"]:
            list_candidates.append(value)

    return jsonify(list_candidates)


@app.route("/addresses", methods=["GET"])
def get_addresses():
    global list_addresses

    list_candidates = list()

    req = request.args.get("req").upper()

    for value in list_addresses:
        if req in value["address"]:
            list_candidates.append(value)
            # if list_candidates.__len__() >= 10:
            #     break

    return jsonify(list_candidates)


if __name__ == '__main__':
    app.run(host="192.168.1.170", port=5000, debug=True)
