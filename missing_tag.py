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

animals = cattle.find_last_worked_cows("LOUISE", "2019-05-11")
print(animals.__len__())
for animal in animals:
    print(animal.ear_tag)



# ear_tags = cattle.match_list_to_cm(r"data/louise_cows.csv")
# for ear_tag in ear_tags:
#     print(ear_tag)
# print(ear_tags.__len__())
#
# ear_tags = cattle.match_cm_to_list(r"data/louise_cows.csv")
# for ear_tag in ear_tags:
#     print(ear_tag)
# print(ear_tags.__len__())
