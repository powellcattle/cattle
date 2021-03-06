#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import cattle
from nosql import mongo_setup

logging.basicConfig(filename="load_animals.log",
                    format="%(asctime)s %(levelname)s:%(message)s",
                    filemode="w",
                    level=logging.DEBUG,
                    datefmt="%m/%d/%Y %I:%M:%S %p")

mongo_setup.global_init()


# db = connect("cattle")
#
cattle.load_pastures(r"data/pastures.csv")
cattle.load_breeds(r"data/breeds.csv")
cattle.load_animals(r"data/animals.csv")
cattle.load_parents(r"data/animals.csv")
cattle.load_children()
cattle.load_treatments(r"data/treatments.csv")
cattle.load_pregnancy_check(r"data/pregnancy_checks.csv")
cattle.load_measurements(r"data/measurements.csv")

# cattle.assign_preg_check()

cattle.load_contacts(r"data/contacts.csv")
cattle.load_breedings(r"data/breedings.csv")

cattle.load_embryos(r"data/embryos.csv")
# cattle.load_movements(r"data/movements.csv")
cattle.load_breeds(r"data/breeds.csv")


# cattle.load_breed_compositions(r"data/breed_compositions.csv")
#
# cattle.create_tru_test(r"data/tru_test_load.csv")
# cattle.create_allflex(r"data/allflex_load.csv")
# cattle.load_measurements(r"data/measurements.csv")
# cattle.load_epds(r"data/epds.csv")

# cattle.sort_tags(r"data/animals.csv")
