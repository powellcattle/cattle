#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect
import logging

import psql_util
from animal_ref import ReferenceAnimal
from nosql.animal import Animal
from nosql.breed import Breed, BreedTemp
from nosql.measurement import Measurement
from nosql.pasture import Pasture
from nosql.pregnancy_check import PregnancyCheck
from treatment import Treatment

__author__ = 'spowell'

import csv
import psycopg2
import sys

import cattle.constants as _sql

import str_util


def load_breeds(_file_name: str) -> None:
    try:
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                breed = BreedTemp()
                breed.id = row[0]
                breed.name = row[2]
                breed.gestation_period = row[3]
                breed.save()

        return None

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info("{} {}".format(inspect.stack()[0][3], "Completed Loading"))


def load_animals(_file_name: str) -> None:
    try:
        ear_tag_colors = ('WHITE', 'BLUE', 'ORANGE', 'YELLOW', 'RED', 'PURPLE', 'CAN')

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                animal = Animal()
                active = str_util.to_upper_or_none(row[25])  # Z
                # if "ACTIVE" != active:
                #     continue
                animal.status = active
                animal.id = str_util.to_pos_int_or_none(row[0])  # A
                animal.ear_tag = str_util.to_upper_or_none(row[3])  # D
                # if not animal.ear_tag:
                #     continue

                animal.ear_tag_loc = str_util.to_upper_or_none(row[4])  # E
                # tattoo_left = str_util.to_upper_or_none(row[5])  # F
                # tattoo_right = str_util.to_upper_or_none(row[6])  # G
                animal.brand = str_util.to_upper_or_none(row[7])  # H
                animal.brand_loc = str_util.to_upper_or_none(row[8])  # I
                # name = str_util.to_upper_or_none(row[9])  # J
                # reg_num = str_util.to_upper_or_none(row[12])  # M
                # reg_num_2 = str_util.to_upper_or_none(row[13])  # N
                animal.other_id = str_util.to_upper_or_none((row[14]))  # O
                # other_id_loc = str_util.to_upper_or_none(row[15])  # P
                animal.electronic_id = str_util.to_upper_or_none(row[16])  # Q
                animal.animal_type = str_util.to_upper_or_none(row[17])  # R
                animal.sex = str_util.to_upper_or_none(row[18])  # S
                breed_id = str_util.to_pos_long_or_none(row[20])  # U

                breed_db = BreedTemp.objects(id=breed_id).first()
                if breed_db:
                    breed = Breed()
                    breed.name = breed_db.name.upper()
                    breed.gestation_period = breed_db.gestation_period
                    animal.breed = breed

                animal.horn_status = str_util.to_upper_or_none(row[21])  # V
                animal.color_markings = str_util.to_upper_or_none(row[22])  # W
                # ocv_tattoo = str_util.to_upper_or_none(row[23])  # X
                # ocv_number = str_util.to_upper_or_none(row[24])  # Y
                animal.status = str_util.to_upper_or_none(row[25])  # Z
                pasture_id = str_util.to_pos_long_or_none(row[26])  # AA
                pasture = Pasture.objects(id=pasture_id).first()
                if pasture:
                    animal.pasture = pasture.name

                animal.birth_date = str_util.to_date_or_none(row[35])  # AJ
                # birth_year = None
                # if birth_date:
                #     birth_year = birth_date.year

                animal.weaning_date = str_util.to_date_or_none(row[36])  # AK
                animal.yearling_date = str_util.to_date_or_none(row[37])  # AL
                animal.conception_method = str_util.to_upper_or_none(row[39])  # AN
                animal.purchase_date = str_util.to_date_or_none(row[41])  # AP
                animal.purchased = str_util.to_boolean_or_none(row[42])  # AQ

                animal.save()

        # con.commit()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info("Done")


def load_parents(_file_name: str) -> None:
    try:
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)

            for row in reader:
                id = str_util.to_pos_int_or_none(row[0])  # A

                animal = Animal.objects(id=id).first()
                if not animal:
                    continue

                # sire
                sire_animal_id = str_util.to_pos_long_or_none(row[27])  # AB
                sire_animal = Animal.objects(id=sire_animal_id).first()
                if sire_animal:
                    ref_animal = ReferenceAnimal(id=sire_animal.id, ear_tag=sire_animal.ear_tag, birth_date=sire_animal.birth_date, status=sire_animal.status)
                    animal.sire_animal = ref_animal
                    animal.save()

                # dam
                dam_animal_id = str_util.to_pos_long_or_none(row[28])  # AC
                dam_animal = Animal.objects(id=dam_animal_id).first()
                if dam_animal:
                    ref_animal = ReferenceAnimal(id=dam_animal.id, ear_tag=dam_animal.ear_tag, birth_date=dam_animal.birth_date, status=dam_animal.status)
                    animal.dam_animal = ref_animal
                    animal.save()

                # genetic dam
                genetic_dam_animal_id = str_util.to_pos_long_or_none(row[29])  # AD
                genetic_dam_animal = Animal.objects(id=genetic_dam_animal_id).first()
                if genetic_dam_animal:
                    ref_animal = ReferenceAnimal(id=genetic_dam_animal.id, ear_tag=genetic_dam_animal.ear_tag, birth_date=genetic_dam_animal.birth_date, status=genetic_dam_animal.status)
                    animal.genetic_dam = ref_animal
                    animal.save()

                # real dam
                real_dam_animal_id = str_util.to_pos_long_or_none(row[30])  # AE
                real_dam_animal = Animal.objects(id=real_dam_animal_id).first()
                if real_dam_animal:
                    ref_animal = ReferenceAnimal(id=real_dam_animal.id, ear_tag=real_dam_animal.ear_tag, birth_date=real_dam_animal.birth_date, status=real_dam_animal.status)
                    animal.genetic_dam = ref_animal
                    animal.save()

    except Exception as e:
        logging.error(f"{inspect.stack()[0][3]} {e}")

    finally:
        logging.info(f"{inspect.stack()[0][3]} Done")


def load_children() -> None:
    animals = Animal.objects()

    for animal in animals:
        if "BULL" == animal.animal_type:
            offspring = Animal.objects(sire_animal__id=animal.id).order_by("-birth_date")
        elif "COW" == animal.animal_type:
            offspring = Animal.objects(dam_animal__id=animal.id).order_by("-birth_date")
        else:
            continue
        if offspring:
            for ref_animal in offspring:
                animal.offspring.append(ReferenceAnimal(
                    id=ref_animal.id,
                    ear_tag=ref_animal.ear_tag,
                    birth_date=ref_animal.birth_date,
                    sex=ref_animal.sex,
                    status=ref_animal.status))
            animal.save()


def assign_preg_check() -> None:
    animals = Animal.objects(animal_type="COW")

    for animal in animals:
        preg_checks = PregnancyCheck.objects(animal_id=animal.id).order_by("-check_date")
        if preg_checks:
            animal.preg_check = preg_checks[0]
            animal.save()


# def load_breedings(_file_name):
#     con = None
#
#     try:
#         con = psycopg2.connect(database='rafter',
#                                user='postgres',
#                                password='postgres',
#                                host='localhost')
#
#         cur = con.cursor()
#         cur.execute(_sql.SQL_DROP_BREEDING)
#         con.commit()
#         cur.execute(_sql.SQL_CREATE_BREEDING)
#         con.commit()
#
#         with open(_file_name, "r") as csvfile:
#             reader = csv.reader(csvfile, delimiter=',', quotechar='"')
#             next(reader, None)
#             for row in reader:
#                 id = str_util.to_pos_int_or_none(row[0])  # A
#                 animal_id = str_util.to_pos_int_or_none(row[1])
#                 bull_animal_id = str_util.to_pos_int_or_none(row[2])
#                 breeding_method = str_util.to_upper_or_none(row[3])
#                 breeding_date = str_util.to_date_or_none(row[4])
#                 breeding_end_date = str_util.to_date_or_none(row[5])
#                 estimated_calving_date = str_util.to_date_or_none(row[7])
#                 cleanup = str_util.to_upper_or_none(row[8])
#                 embryo_id = str_util.to_pos_int_or_none(row[9])
#                 pregnancy_check_id = str_util.to_pos_int_or_none(row[17])
#
#                 cur.execute(_sql.SQL_INSERT_BREEDING, (
#                     id,
#                     animal_id,
#                     bull_animal_id,
#                     breeding_method,
#                     breeding_date,
#                     breeding_end_date,
#                     estimated_calving_date,
#                     cleanup,
#                     embryo_id,
#                     pregnancy_check_id))
#                 con.commit()
#
#     except psycopg2.DatabaseError as e:
#         sys.exit(1)
#
#     else:
#         sys.exit(0)
#
#     finally:
#
#


def load_embryos(_file_name):
    con = None
    csvfile = None

    try:
        con = psql_util.psql_connection(_host="192.168.1.130", _database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_EMBRYOS)
        con.commit()
        cur.execute(_sql.SQL_CREATE_EMBRYOS)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                id = str_util.to_pos_int_or_none(row[0])  # A
                dam_id = str_util.to_pos_int_or_none(row[2])  # C
                sire_id = str_util.to_pos_int_or_none(row[3])  # D
                cur.execute(_sql.SQL_INSERT_EMBRYOS, (
                    id,
                    sire_id,
                    dam_id))
                con.commit()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_movements(_file_name):
    csvfile = None
    con = None

    try:
        con = psql_util.psql_connection(_host="192.168.1.130", _database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_MOVEMENTS)
        con.commit()
        cur.execute(_sql.SQL_CREATE_MOVEMENTS)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                id = str_util.to_pos_int_or_none(row[0])  # A
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                moved_from_pasture_id = str_util.to_pos_int_or_none(row[2])  # C
                moved_to_pasture_id = str_util.to_pos_int_or_none(row[3])  # D
                movement_date = str_util.to_date_or_none(row[4])  # E
                cur.execute(_sql.SQL_INSERT_MOVEMENTS, (
                    id,
                    animal_id,
                    moved_from_pasture_id,
                    moved_to_pasture_id,
                    movement_date))
                con.commit()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def create_tru_test(_csv_file):
    con = None
    f = None
    try:
        f = open(_csv_file, 'wt')
        writer = csv.writer(f)
        writer.writerow(("VID", "EID", "LID", "Breed", "Sex", "Color"))
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(_sql.SQL_TRUE_TEST)
        rows = cur.fetchall()

        for row in rows:
            vid = row[0]
            eid = row[1]
            breed = row[2]
            lid = row[3]
            color = row[5]

            animal_type = row[4]
            sex = row[6]

            if animal_type == 'CALF':
                if sex == 'HEIFER':
                    sex = 'HEIFER CALF'
                elif sex == "STEER":
                    sex = 'STEER CALF'
                elif sex == 'BULL':
                    sex = 'BULL CALF'
                else:
                    sex = 'UNKNOWN CALF'
            else:
                sex = animal_type

            writer.writerow((vid, eid, sex, breed, lid, color))

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()
        f.close()


def create_allflex(_csv_file):
    con = None
    delim = '-'

    f = None
    try:
        f = open(_csv_file, 'wt')
        writer = csv.writer(f)
        writer.writerow(("EID", "VID", "LID", "OTH"))
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(_sql.SQL_SELECT_ALLFLEX)
        rows = cur.fetchall()

        for row in rows:
            vid = row[0]
            eid = row[1]
            brd = row[2]
            lid = row[3]
            col = row[5]
            hst = row[7]

            # build composite field
            oth = None
            if abv_breed(brd) is not None:
                oth = abv_breed(brd)
            if abv_color(col) is not None:
                if oth is not None:
                    oth = oth + delim + abv_color(col)
                else:
                    oth = abv_color(col)
            if abv_horned(hst) is not None:
                if oth is not None:
                    oth = oth + delim + abv_horned(hst)
                else:
                    oth = abv_horned(hst)

            writer.writerow((eid, vid, lid, oth))

    except psycopg2.DatabaseError as e:
        sys.exit(1)

    finally:
        if con:
            con.close()
        f.close()


def abv_color(_color):
    color = None

    if _color is None:
        return color

    _color = _color.upper()
    if _color == "BLACK W/MOTTLED WHITE FACE":
        color = "BWF"
    elif _color == "BLACK W/WHITE MOTTLED THROAT":
        color = "BWF"
    elif _color == "BRINDLE":
        color = "BRD"
    elif _color == "DARK GREY":
        color = "DG"
    elif _color == "LIGHT RED":
        color = "LR"
    elif _color == "RED & WHITE FACE":
        color = "RWF"
    elif _color == "RED W/MOTTLED FACE":
        color = "RMF"
    elif _color == "SOLID BLACK":
        color = "B"
    elif _color == "SOLID BLACK W/WHITE FACE":
        color = "BWF"
    elif _color == "SOLID GREY":
        color = "G"
    elif _color == "SOLID RED":
        color = "R"
    elif _color == "SOLID WHITE":
        color = "W"
    elif _color == "SOLID YELLOW":
        color = "Y"
    return color


def abv_breed(_breed):
    breed = None

    if _breed is None:
        return breed

    _breed = _breed.upper()
    if _breed == "ANGUS":
        breed = "AS"
    elif _breed == "BRAHMAN":
        breed = "BN"
    elif _breed == "BRANGUS":
        breed = "BS"
    elif _breed == "BRANGUS F1":
        breed = "B1"
    elif _breed == "CHAROLAIS":
        breed = "CH"
    elif _breed == "COMMERCIAL":
        breed = "CM"
    elif _breed == "HEREFORD":
        breed = "HD"
    return breed


def abv_horned(_horned):
    horned = None

    if _horned is None:
        return horned

    _horned = _horned.upper()
    if _horned == "HORNED":
        horned = "H"
    elif _horned == "POLLED":
        horned = "P"
    elif _horned == "SCURRED":
        horned = "S"
    elif _horned == "DEHORNED":
        horned = "B1"
    elif _horned == "CHAROLAIS":
        horned = "D"
    return horned


def load_contacts(_file_name):
    con = None
    csvfile = None

    try:
        con = psql_util.psql_connection(_host="192.168.1.130", _database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_CONTACT)
        con.commit()
        cur.execute(_sql.SQL_CREATE_CONTACT)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                contact_id = str_util.to_pos_int_or_none(row[0])  # A
                name = str_util.to_upper_or_none(row[8])

                cur.execute(_sql.SQL_INSERT_CONTACT, (
                    contact_id,
                    name))
                con.commit()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_pastures(_file_name):
    try:
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                pasture = Pasture()
                pasture.id = str_util.to_pos_int_or_none(row[0])  # A
                pasture.name = str_util.to_upper_or_none(row[3])  # D
                pasture.premise_id = str_util.to_upper_or_none(row[4])  # E
                pasture.acres = str_util.to_float_or_none(row[5])  # F
                pasture.save()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if csvfile:
            csvfile.close()


def load_epds(_file_name):
    con = None

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_EPDS)
        con.commit()
        cur.execute(_sql.SQL_CREATE_EPDS)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                id = str_util.to_pos_int_or_none(row[0])  # A
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                epd_reporting_period = str_util.to_upper_or_none(row[2])  # C
                epd_type = str_util.to_upper_or_none((row[3]))  # D
                ced_epd = str_util.to_float_or_none(row[4])  # E
                ced_acc = str_util.to_float_or_none(row[33])  # AH
                bw_epd = str_util.to_float_or_none(row[5])  # F
                bw_acc = str_util.to_float_or_none(row[34])  # AI
                ww_epd = str_util.to_float_or_none(row[6])  # G
                ww_acc = str_util.to_float_or_none(row[35])  # AJ
                yw_epd = str_util.to_float_or_none(row[7])  # H
                yw_acc = str_util.to_float_or_none(row[36])  # AK
                milk_epd = str_util.to_float_or_none(row[10])  # K
                milk_acc = str_util.to_float_or_none(row[39])  # AN
                mww_epd = str_util.to_float_or_none(row[12])  # K
                mww_acc = str_util.to_float_or_none(row[41])  # AN

                cur.execute(_sql.SQL_INSERT_EPDS, (
                    id,
                    animal_id,
                    epd_reporting_period,
                    epd_type,
                    ced_epd,
                    ced_acc,
                    bw_epd,
                    bw_acc,
                    ww_epd,
                    ww_acc,
                    yw_epd,
                    yw_acc,
                    milk_epd,
                    milk_acc,
                    mww_epd,
                    mww_acc))
                con.commit()

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_treatments(_file_name):
    con = None

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_TREATMENTS)
        con.commit()
        cur.execute(_sql.SQL_CREATE_TREATMENTS)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                id = str_util.to_pos_int_or_none(row[0])  # A
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                treatment_date = str_util.to_date_or_none(row[2])  # C
                medication = str_util.to_upper_or_none((row[6]))  # D

                cur.execute(_sql.SQL_INSERT_TREATMENTS, (
                    id,
                    animal_id,
                    treatment_date,
                    medication))
                con.commit()

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_measurements(_file_name):
    con = None

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_MEASUREMENTS)
        con.commit()
        cur.execute(_sql.SQL_CREATE_MEASUREMENTS)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                id = str_util.to_pos_int_or_none(row[0])  # A
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                category = str_util.to_upper_or_none(row[2])  # C
                measure_date = str_util.to_date_or_none((row[3]))  # D
                age_at_measure = str_util.to_pos_int_or_none(row[4])  # E
                weight = str_util.to_pos_int_or_none(row[5])  # F
                adjusted_weight = str_util.to_pos_int_or_none(row[6])  # G
                adg = str_util.to_float_or_none(row[8])  # I
                wda = str_util.to_float_or_none(row[10])  # K
                reference_weight = str_util.to_pos_int_or_none(row[19])  # T
                gain = str_util.to_pos_int_or_none(row[20])  # U
                scrotal = str_util.to_float_or_none(row[16])  # Q

                cur.execute(_sql.SQL_INSERT_MEASUREMENTS, (
                    id,
                    animal_id,
                    category,
                    measure_date,
                    age_at_measure,
                    weight,
                    adjusted_weight,
                    adg,
                    wda,
                    reference_weight,
                    gain,
                    scrotal))
                con.commit()

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_breed_compositions(_file_name):
    csvfile = None
    con = None

    try:
        con = psql_util.psql_connection(_host="192.168.1.130", _database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_BREED_COMPOSITIONS)
        con.commit()
        cur.execute(_sql.SQL_CREATE_BREED_COMPOSITIONS)
        con.commit()

        dict = dict()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                dict["id"] = str_util.to_pos_int_or_none(row[0])  # A
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                breed_id = str_util.to_pos_int_or_none(row[2])  # C
                percentage = str_util.to_float_or_none(row[3])  # D

                # cur.execute(_sql.SQL_INSERT_BREED_COMPOSITIONS, (
                #     id,
                #     animal_id,
                #     breed_id,
                #     percentage))

            con.commit()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_calves(_file_name):
    con = None
    csvfile = None

    try:
        # breeding_forms = load_animal_custom_fields("BREEDING FORM")
        color_DNAs = load_animal_custom_fields("COAT COLOR DNA")
        breeds = load_breeds_map()
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_CALF)
        con.commit()
        cur.execute(_sql.SQL_CREATE_CALF)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                active = str_util.to_upper_or_none(row[25])  # Z
                if active != "ACTIVE":
                    continue
                animal_type = str_util.to_upper_or_none(row[17])
                if animal_type != "CALF":
                    continue

                id = str_util.to_pos_int_or_none(row[0])  # A
                sire_id = str_util.to_pos_int_or_none(row[27])  # AB
                dam_id = str_util.to_pos_int_or_none(row[28])  # AC
                real_dam_id = str_util.to_pos_int_or_none(row[30])  # AE
                # breed
                breed_key = str_util.to_pos_int_or_none(row[20])  # U
                breed = ec_hashmap.get(breeds, breed_key)

                coat_color_dna = ec_hashmap.get(color_DNAs, id)
                if coat_color_dna:
                    if "ED/ED" in coat_color_dna:
                        coat_color_dna = "ED/ED"
                    elif "ED/E" in coat_color_dna:
                        coat_color_dna = "ED/E"
                    elif "NOT TESTED" in coat_color_dna:
                        coat_color_dna = "NOT TESTED"
                    else:
                        coat_color_dna = None

                ear_tag = str_util.to_upper_or_none(row[3])  # D
                if ear_tag is None:
                    continue
                sex = str_util.to_upper_or_none(row[18])
                dob_date = str_util.to_upper_or_none(row[35])
                birth_weight = str_util.to_pos_int_or_none(row[69])
                weaning_weight = str_util.to_pos_int_or_none(row[70])
                yearling_weight = str_util.to_pos_int_or_none(row[71])
                adj_birth_weight = str_util.to_pos_int_or_none(row[72])
                adj_weaning_weight = str_util.to_pos_int_or_none(row[73])
                adj_yearling_weight = str_util.to_pos_int_or_none(row[74])

                # seller_id = str_util.to_pos_int_or_none(row[43])  # AR
                # current_breeding_status = str_util.to_upper_or_none(row[59])  # BH
                # last_calving_date = str_util.to_date_or_none(row[58])
                # estimated_calving_date = str_util.to_date_or_none(row[60])
                # last_breeding_date = str_util.to_date_or_none(row[58])
                # contact_id = str_util.to_pos_int_or_none(row[43])  # AR
                # dob = str_util.to_date_or_none(row[35])

                cur.execute(_sql.SQL_INSERT_CALF, (
                    id,
                    sire_id,
                    dam_id,
                    real_dam_id,
                    sex,
                    breed,
                    coat_color_dna,
                    dob_date,
                    ear_tag,
                    birth_weight,
                    weaning_weight,
                    yearling_weight,
                    adj_birth_weight,
                    adj_weaning_weight,
                    adj_yearling_weight))
                con.commit()

    except psycopg2.DatabaseError as e:
        sys.exit(1)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_cows(_file_name):
    con = None
    csvfile = None

    try:
        # breedings = cattle.load_breedings()
        breeding_forms = load_animal_custom_fields("BREEDING FORM")
        color_DNAs = load_animal_custom_fields("COAT COLOR DNA")
        breeds = load_breeds_map()

        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_COW)
        con.commit()
        cur.execute(_sql.SQL_CREATE_COW)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                active = str_util.to_upper_or_none(row[25])  # Z
                if active != "ACTIVE" and active != "REFERENCE":
                    continue
                id = str_util.to_pos_int_or_none(row[0])  # A
                sire_id = str_util.to_pos_int_or_none(row[27])  # AB
                dam_id = str_util.to_pos_int_or_none(row[28])  # AC
                real_dam_id = str_util.to_pos_int_or_none(row[30])  # AE
                # breed
                breed_key = str_util.to_pos_int_or_none(row[20])  # U
                breed = ec_hashmap.get(breeds, breed_key)
                breeding_type = ec_hashmap.get(breeding_forms, id)
                if breeding_type:
                    if "FLUSH" in breeding_type:
                        breeding_type = "FLUSH"
                    elif "AI" in breeding_type:
                        breeding_type = "AI"
                    elif "NS" in breeding_type:
                        breeding_type = "NS"
                    elif "RECIPIENT" in breeding_type:
                        breeding_type = "RECIPIENT"
                    else:
                        breeding_type = None

                coat_color_dna = ec_hashmap.get(color_DNAs, id)
                if coat_color_dna:
                    if "ED/ED" in coat_color_dna:
                        coat_color_dna = "ED/ED"
                    elif "ED/E" in coat_color_dna:
                        coat_color_dna = "ED/E"
                    elif "NOT TESTED" in coat_color_dna:
                        coat_color_dna = "NOT TESTED"
                    else:
                        coat_color_dna = None

                ear_tag = str_util.to_upper_or_none(row[3])  # D
                if ear_tag is None:
                    continue
                animal_type = str_util.to_upper_or_none(row[17])
                sex = str_util.to_upper_or_none(row[18])
                dob_date = str_util.to_upper_or_none(row[35])
                dob_year = None
                if dob_date:
                    dob_year = dob_date.split("-")[0]

                seller_id = str_util.to_pos_int_or_none(row[43])  # AR
                current_breeding_status = str_util.to_upper_or_none(row[59])  # BH
                last_calving_date = str_util.to_date_or_none(row[58])  # BG
                estimated_calving_date = str_util.to_date_or_none(row[60])  # BI
                last_breeding_date = str_util.to_date_or_none(row[58])
                contact_id = str_util.to_pos_int_or_none(row[43])  # AR
                dob = str_util.to_date_or_none(row[35])

                cur.execute(_sql.SQL_INSERT_COW, (
                    id,
                    active,
                    sire_id,
                    dam_id,
                    real_dam_id,
                    breed,
                    breeding_type,
                    coat_color_dna,
                    current_breeding_status,
                    dob,
                    ear_tag,
                    estimated_calving_date,
                    last_breeding_date,
                    last_calving_date,
                    contact_id))
                con.commit()

    except psycopg2.DatabaseError as e:
        sys.exit(1)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_bulls(_file_name):
    con = None
    csvfile = None

    try:
        breeding_forms = load_animal_custom_fields("BREEDING FORM")
        color_DNAs = load_animal_custom_fields("COAT COLOR DNA")
        breeds = load_breeds_map()

        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_BULL)
        con.commit()
        cur.execute(_sql.SQL_CREATE_BULL)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                active = str_util.to_upper_or_none(row[25])  # Z
                if active != "ACTIVE" and active != "REFERENCE":
                    continue
                id = str_util.to_pos_int_or_none(row[0])  # A
                sire_id = str_util.to_pos_int_or_none(row[27])  # AB
                dam_id = str_util.to_pos_int_or_none(row[28])  # AC
                real_dam_id = str_util.to_pos_int_or_none(row[30])  # AE
                # breed
                breed_key = str_util.to_pos_int_or_none(row[20])  # U
                breed = ec_hashmap.get(breeds, breed_key)
                breeding_type = ec_hashmap.get(breeding_forms, id)
                if breeding_type:
                    if "FLUSH" in breeding_type:
                        breeding_type = "FLUSH"
                    elif "AI" in breeding_type:
                        breeding_type = "AI"
                    elif "NS" in breeding_type:
                        breeding_type = "NS"
                    elif "RECIPIENT" in breeding_type:
                        breeding_type = "RECIPIENT"
                    else:
                        breeding_type = None

                coat_color_dna = ec_hashmap.get(color_DNAs, id)
                if coat_color_dna:
                    if "ED/ED" in coat_color_dna:
                        coat_color_dna = "ED/ED"
                    elif "ED/E" in coat_color_dna:
                        coat_color_dna = "ED/E"
                    elif "NOT TESTED" in coat_color_dna:
                        coat_color_dna = "NOT TESTED"
                    else:
                        coat_color_dna = None

                ear_tag = str_util.to_upper_or_none(row[3])  # D
                animal_type = str_util.to_upper_or_none(row[17])
                sex = str_util.to_upper_or_none(row[18])
                dob_date = str_util.to_upper_or_none(row[35])
                dob_year = None
                if dob_date:
                    dob_year = dob_date.split("-")[0]

                seller_id = str_util.to_pos_int_or_none(row[43])  # AR
                current_breeding_status = str_util.to_upper_or_none(row[59])  # BH
                last_calving_date = str_util.to_date_or_none(row[58])  # BG
                estimated_calving_date = str_util.to_date_or_none(row[60])  # BI
                last_breeding_date = str_util.to_date_or_none(row[58])
                contact_id = str_util.to_pos_int_or_none(row[43])  # AR
                dob = str_util.to_date_or_none(row[35])

                cur.execute(_sql.SQL_INSERT_BULL, (
                    id,
                    sire_id,
                    dam_id,
                    real_dam_id,
                    breed,
                    breeding_type,
                    coat_color_dna,
                    current_breeding_status,
                    dob,
                    ear_tag,
                    contact_id))
                con.commit()

    except psycopg2.DatabaseError as e:
        sys.exit(1)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_sale_tickets():
    sale_tickets = ec_hashmap.new()

    try:
        with open("../data/cattle/sale_tickets.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                key = str_util.to_pos_int_or_none(row[0])
                sale_date = str_util.to_upper_or_none(row[6])
                if sale_date:
                    sale_year = int(sale_date.split("-")[0])
                    sale_month = int(sale_date.split("-")[1])
                    sale_day = int(sale_date.split("-")[2])
                ec_hashmap.set(sale_tickets, key, [sale_year, sale_month, sale_day])

    finally:
        if csvfile:
            csvfile.close()

    return sale_tickets


def load_animal_custom_fields(_field_name=None):
    if _field_name is None:
        return

    custom_fields = dict()

    try:
        with open("data/cattle/animal_custom_fields.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                field_name = str_util.to_upper_or_none(row[2])
                if field_name == _field_name.upper():
                    key = str_util.to_pos_int_or_none(row[1])
                    value = str_util.to_upper_or_none(row[3])
                    custom_fields[key] = value
    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if csvfile:
            csvfile.close()

    return custom_fields


def load_breeds_map():
    breeds = dict()

    try:
        with open("data/cattle/breeds.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                key = str_util.to_pos_int_or_none(row[0])
                name = str_util.to_upper_or_none(row[2])
                breeds[key] = name

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if csvfile:
            csvfile.close()

    return breeds


def hashmap_contacts():
    contacts = ec_hashmap.new()

    csvfile = None
    try:
        with open("../data/cattle/contacts.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                key = str_util.to_pos_int_or_none(row[0])
                name = str_util.to_upper_or_none(row[8])
                ec_hashmap.set(contacts, key, name)

    finally:
        if csvfile:
            csvfile.close()

    return contacts


def write_dead(_dead, _year):
    csvfile = None
    try:
        file_name = "../data/cattle/rc_dead_" + str(_year) + ".csv"
        with open(file_name, "w") as csvfile:
            wr = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            row = ["ID", "EAR TAG", "TYPE", "SEX", "DOB", "BREED", "YEAR DEATH"]
            wr.writerow(row)

            for death in _dead:
                if int(death.death_year) == _year:
                    row = [death.animal_id, death.ear_tag, death.animal_type, death.animal_sex, death.birth_year,
                           death.breed, death.death_year]
                    wr.writerow(row)
    finally:
        if csvfile:
            csvfile.close()


def write_sold(_sales, _year):
    csvfile = None
    try:
        file_name = "../data/cattle/rc_sales_" + str(_year) + ".csv"
        with open(file_name, "w") as csvfile:
            wr = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # write csv cell headers
            wr.writerow(["ID", "EAR TAG", "TYPE", "SEX", "DOB", "BREED", "SOLD YEAR", "SALE AMOUNT"])

            for sale in _sales:
                if int(sale.year_sold) == _year:
                    wr.writerow([sale.animal_id, sale.ear_tag, sale.animal_type, sale.animal_sex, sale.birth_year, sale.breed, sale.year_sold, sale.amount])
    finally:
        if csvfile:
            csvfile.close()


def write_purchased(_purchases, _year):
    csvfile = None
    try:
        file_name = "../data/cattle/rc_purchased_" + str(_year) + ".csv"
        with open(file_name, "w") as csvfile:
            wr = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            row = ["ID", "EAR TAG", "TYPE", "SEX", "DOB", "BREED", "PURCHASE YEAR", "PURCHASE AMOUNT", "SELLER"]
            wr.writerow(row)

            for purchase in _purchases:
                if int(purchase.purchase_year) == _year:
                    row = [purchase.animal_id, purchase.ear_tag, purchase.animal_type, purchase.animal_sex,
                           purchase.birth_year, purchase.breed, purchase.purchase_year, purchase.amount,
                           purchase.seller_name]
                    wr.writerow(row)
    finally:
        if csvfile:
            csvfile.close()


def write_inventory(_inventories, _year):
    csvfile = None

    try:
        file_name = "../data/cattle/rc_inventory_" + str(_year) + ".csv"
        with open(file_name, "w") as csvfile:
            wr = csv.writer(csvfile, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

            row = ["ID", "EAR TAG", "TYPE", "SEX", "DOB", "BREED"]
            wr.writerow(row)

            for inventory in _inventories:
                row = [inventory.animal_id, inventory.ear_tag, inventory.animal_type, inventory.animal_sex,
                       inventory.birth_year, inventory.breed]
                wr.writerow(row)
    finally:
        if csvfile:
            csvfile.close()


def load_breedings(_file_name):
    con = None
    csvfile = None

    # dict = dict()

    try:
        con = psql_util.psql_connection(_host="192.168.1.130", _database='rafter', _user='postgres', _password='postgres')

        cur = con.cursor()
        cur.execute(_sql.SQL_DROP_BREEDING)
        con.commit()
        cur.execute(_sql.SQL_CREATE_BREEDING)
        con.commit()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                # id
                id = str_util.to_pos_int_or_none(row[0])
                animal_id = str_util.to_pos_int_or_none(row[1])
                bull_animal_Id = str_util.to_pos_int_or_none(row[2])
                breeding_method = str_util.to_upper_or_none(row[3])
                breeding_date = str_util.to_date_or_none(row[4])
                breeding_end_date = str_util.to_date_or_none(row[5])
                days_exposed = str_util.to_pos_int_or_none(row[6])
                estimated_calving_date = str_util.to_date_or_none(row[7])
                cleanup = str_util.to_boolean_or_none(row[8])
                embryo_id = str_util.to_pos_int_or_none(row[9])
                embryo_cl_side = str_util.to_upper_or_none(row[10])
                pregnancy_check_id = str_util.to_pos_int_or_none(row[17])

                cur.execute(_sql.SQL_INSERT_BREEDING, (
                    id,
                    animal_id,
                    bull_animal_Id,
                    breeding_method,
                    breeding_date,
                    breeding_end_date,
                    estimated_calving_date,
                    cleanup,
                    embryo_id,
                    pregnancy_check_id))
                con.commit()


    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def load_pregnancy_check(_file_name):
    try:
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                preg_check = PregnancyCheck()
                animal_id = str_util.to_pos_int_or_none(row[1])
                animal = Animal.objects(id=animal_id).first()
                if not animal:
                    continue
                preg_check.id = str_util.to_pos_int_or_none(row[0])
                preg_check.check_date = str_util.to_date_or_none(row[2])
                preg_check.check_method = str_util.to_upper_or_none(row[3])
                preg_check.result = str_util.to_upper_or_none(row[4])
                preg_check.expected_due_date = str_util.to_date_or_none(row[7])
                preg_check.comments = str_util.to_upper_or_none(row[8])
                animal.preg_checks.append(preg_check)
                animal.save()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        if csvfile:
            csvfile.close()


def set_row_to_animal(_row):
    animal = None
    if _row is not None:
        animal = Animal()
        animal.setAnimalId(_row[0])
        animal.setEarTag(str(_row[1]))
        animal.setAnimalSex(str_util.to_upper_or_none(_row[13]))
        animal.setSireId(_row[22])
        animal.setRealDamId(_row[25])
        animal.setName(str_util.to_upper_or_none(_row[7]))
        animal.setRegNum(str_util.to_upper_or_none(_row[8]))
        animal.animal_type = str_util.to_upper_or_none(_row[13])
        animal.color_markings = str_util.to_upper_or_none(_row[17])
        animal.horn_status = str_util.to_upper_or_none(_row[16])
        animal.eid = str_util.to_upper_or_none(_row[12])
        animal.conception_method = str_util.to_upper_or_none(_row[35])
        animal.dob = _row[30]
        animal.dow = _row[32]
        animal.doy = _row[33]
        animal.breed = _row[87]
        animal.breed_percentage = _row[88]
        if (_row[5] is not None):
            animal.brand = _row[5]
            animal.brand_loc = _row[6]
            if (_row[6] is not None):
                animal.brand = _row[5] + "/" + _row[6]

    return animal


def lookup_animal_by_id(_animalid):
    con = None
    if _animalid is None:
        return None

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        sql = _sql.SQL_SELECT_ANIMAL + \
              " LEFT OUTER JOIN cattle.breeds AS b ON a.breed_id = b.id" + \
              " LEFT OUTER JOIN cattle.breed_compositions AS bc ON (a.id = bc.animal_id AND a.breed_id = bc.breed_id) " + \
              " WHERE a.id = " + str(_animalid)

        cur.execute(_sql.SQL)
        row = cur.fetchone()
        animal = set_row_to_animal(row)
        con.commit()
        return (animal)

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def lookup_animal_by_ear_tag(_ear_tag):
    con = None

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()
        s = _sql.SQL_SELECT_ANIMAL + \
            " LEFT OUTER JOIN cattle.breeds AS b ON a.breed_id = b.id" + \
            " LEFT OUTER JOIN cattle.breed_compositions AS bc ON (a.id = bc.animal_id AND a.breed_id = bc.breed_id) " + \
            " WHERE a.ear_tag='" + str(_ear_tag) + "'"
        cur.execute(s)
        row = cur.fetchone()
        animal = set_row_to_animal(row)
        con.commit()

        return (animal)

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def create_customer_report(_ear_tag):
    con = None
    source = 'http://cgenregistry.cloudapp.net/CCA/graphics'

    try:
        animal = lookup_animal_by_ear_tag(_ear_tag)
        if animal is None:
            return

        s = lookup_animal_by_id(animal.getSireId())
        d = None
        d = lookup_animal_by_id(animal.getRealDamId())
        if s is not None and s.getSireId() is not None:
            ss = lookup_animal_by_id(s.getSireId())
        dss = None
        if ss is not None and ss.getRealDamId() is not None:
            dss = lookup_animal_by_id(ss.getRealDamId())
        sss = None
        if ss is not None and ss.getSireId() is not None:
            sss = lookup_animal_by_id(ss.getSireId())
        ds = None
        if s is not None and s.getSireId() is not None:
            ds = lookup_animal_by_id(s.getRealDamId())
        sds = None
        if ds is not None and ds.getSireId() is not None:
            sds = lookup_animal_by_id(ds.getSireId())
        dds = None
        if ds is not None and ds.getRealDamId() is not None:
            dds = lookup_animal_by_id(ds.getRealDamId())
        sd = None
        if d is not None and d.getSireId() is not None:
            sd = lookup_animal_by_id(d.getSireId())
        ssd = None
        if sd is not None and sd.getSireId() is not None:
            ssd = lookup_animal_by_id(sd.getSireId())
        dsd = None
        if sd is not None and sd.getRealDamId() is not None:
            dsd = lookup_animal_by_id(sd.getRealDamId())
        dd = None
        if d is not None and d.getRealDamId() is not None:
            dd = lookup_animal_by_id(d.getRealDamId())
        sdd = None
        if dd is not None and dd.getSireId() is not None:
            sdd = lookup_animal_by_id(dd.getSireId())
        ddd = None
        if dd is not None and dd.getRealDamId() is not None:
            ddd = lookup_animal_by_id(dd.getRealDamId())

        h = ''
        title = ""
        if animal.getName() is None:
            title = str(animal.eid)
        else:
            title = str(animal.getName())

        # General
        h += '<table align="center" cellspacing="0" cellpadding="1" border="0" style="border-color:#6fa527;border-width:1px;border-style:ridge;width:394px;border-collapse:collapse;">'
        h += '<tr align="left">'
        h += '<td colspan="3" style="font-weight:bold;color:White;background-color:#6fa527;border-color:#6fa527;border-width:2px;border-style:ridge;">'
        h += 'General: ' + title
        h += '</td>'
        h += '</tr>'
        h += create_general_html_row(animal)
        h += '</table>'
        h += '&nbsp;'
        # h += '<p style="page-break-before:always">'
        # Pedigree
        h += '<table align="center" cellspacing="0" cellpadding="2" border="0" style="border-color:#6fa527;border-width:2px;border-style:ridge;width:786px;border-collapse:collapse;">'
        h += '<tr>'
        h += '<td  align="left" colspan="4" style="font-weight:bold;color:White;background-color:#6fa527;border-color:#6fa527;border-width:2px;border-style:ridge;">'
        h += 'Pedigree: ' + title
        h += '</td>'
        h += '</tr>'
        h += '<tr>'
        h += '<td style="width:100px;"></td>'
        h += '<td style="width:100px;"></td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/sirebar.gif">'
        h += '</td>'
        h += '<td style="width:486px;" align="left" >'
        h += '<a id="sssreg" href="#">'
        if sss is not None and sss.getRegNum() is not None:
            h += sss.getRegNum()
        h += '</a>'
        h += '<span id="sssname">  '
        if sss is not None and sss.getName() is not None:
            h += sss.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr>'
        h += '<tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/sirebar.gif">'
        h += '</td>'
        h += '<td align="left" colspan="2" style="width:586px;">'
        h += '<a id="ssreg" href="#">'
        if ss is not None and ss.getRegNum() is not None:
            h += ss.getRegNum()
        else:
            h += ''
        h += '</a>'
        h += '<span id="ssname">  '
        if ss is not None and ss.getName() is not None:
            h += ss.getName()
        else:
            h += ''
        h += '</span>'
        h += '</td>'
        h += '</tr>'
        h += '<tr>'
        h += '<td style="width:100px;"></td><td style="width:100px;"></td><td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/dambar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="dssreg" href="#">'
        if dss is not None and dss.getRegNum() is not None:
            h += dss.getRegNum()
        else:
            h += ''
        h += '</a>'
        h += '<span id="dssname">'
        if dss is not None and dss.getName() is not None:
            h += dss.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td align="center" style="width:100px;">Sire:</td>'
        h += '<td align="left" colspan="3" style="width:686px;">'
        h += '<a id="sreg" href="#">'
        if s is not None and s.getRegNum() is not None:
            h += s.getRegNum()
        h += '</a>'
        h += '<span id="sname">  '
        if s is not None and s.getName() is not None:
            h += s.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/sirebar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="sdsreg" href="">'
        if sds is not None and sds.getRegNum() is not None:
            h += sds.getRegNum()
        h += '</a>'
        h += '<span id="sdsname">  '
        if sds is not None and sds.getName() is not None:
            h += sds.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/dambar.gif">'
        h += '</td>'
        h += '<td align="left" colspan="2" style="width:586px;">'
        h += '<a id="dsreg" href="#">'
        if ds is not None and ds.getRegNum() is not None:
            h += ds.getRegNum()
        h += '</a>'
        h += '<span id="dsname">  '
        if ds is not None and ds.getName() is not None:
            h += ds.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/dambar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="ddsreg" href="#">'
        if dds is not None and dds.getRegNum() is not None:
            h += dds.getRegNum()
        h += '</a>'
        h += '<span id="ddsname">  '
        if dds is not None and dds.getName() is not None:
            h += dds.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td colspan="4" style="width:786px;"></td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/sirebar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="ssdreg" href="#">'
        if ssd is not None and ssd.getRegNum() is not None:
            h += ssd.getRegNum()
        h += '</a>'
        h += '<span id="ssdname">  '
        if ssd is not None and ssd.getName() is not None:
            h += ssd.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/sirebar.gif">'
        h += '</td>'
        h += '<td align="left" colspan="2" style="width:586px;">'
        h += '<a id="sdreg" href="#">'
        if sd is not None and sd.getRegNum() is not None:
            h += sd.getRegNum()
        h += '</a>'
        h += '<span id="sdname">  '
        if sd is not None and sd.getName() is not None:
            h += sd.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/dambar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="dsdreg" href="#">'
        if dsd is not None and dsd.getRegNum() is not None:
            h += dsd.getRegNum()
        h += '</a>'
        h += '<span id="dsdname">  '
        if dsd is not None and dsd.getName() is not None:
            h += dsd.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td align="center" style="width:100px;">Dam:</td>'
        h += '<td align="left" colspan="3" style="width:686px;">'
        h += '<a id="dreg" href="#">'
        if d is not None and d.getRegNum() is not None:
            h += d.getRegNum()
        h += '</a>'
        h += '<span id="dname">  '
        if d is not None and d.getName() is not None:
            h += d.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/sirebar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="sddreg" href="#">'
        if sdd is not None and sdd.getRegNum() is not None:
            h += sdd.getRegNum()
        h += '</a>'
        h += '<span id="sddname">  '
        if sdd is not None and sdd.getName() is not None:
            h += sdd.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/dambar.gif">'
        h += '</td>'
        h += '<td align="left" colspan="2" style="width:586px;">'
        h += '<a id="ddreg" href="#">'
        if dd is not None and dd.getRegNum() is not None:
            h += dd.getRegNum()
        h += '</a>'
        h += '<span id="ddname">  '
        if dd is not None and dd.getName() is not None:
            h += dd.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr><tr>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td style="width:100px;">'
        h += '</td>'
        h += '<td align="right" style="width:100px;">'
        h += '<IMG alt="" src="' + source + '/dambar.gif">'
        h += '</td>'
        h += '<td align="left" style="width:486px;">'
        h += '<a id="dddreg" href="#">'
        if ddd is not None and ddd.getRegNum() is not None:
            h += ddd.getRegNum()
        h += '</a>'
        h += '<span id="dddname">  '
        if ddd is not None and ddd.getName() is not None:
            h += ddd.getName()
        h += '</span>'
        h += '</td>'
        h += '</tr>'
        h += '</table>'
        h += '&nbsp;'
        # h += '<p style="page-break-before:always">'

        # Measurements
        h += '<table align="center" cellspacing="0" cellpadding="2" border="0" style="border-color:#6fa527;border-width:2px;border-style:ridge;width:786px;border-collapse:collapse;">'
        h += '<tr>'
        h += '<td  align="left" colspan="4" style="font-weight:bold;color:White;background-color:#6fa527;border-color:#6fa527;border-width:2px;border-style:ridge;">'
        h += 'Measurements: ' + title
        h += '</td>'
        h += '</tr>'
        h += '<tr align="left" style="font-weight:bold;color:black;background-color:#f2f2f2;">'
        h += '<td>Date</td>'
        h += '<td>Weight</td>'
        h += '<td>Gain</td>'
        if animal.getAnimalSex() == "BULL":
            h += '<td>Scrotal</td>'
        else:
            h += '<td></td>'
        h += '</tr>'
        h += create_measurements_html_row(_ear_tag)
        h += '</table>'
        h += '&nbsp;'
        # h += '<p style="page-break-before:always">'

        # EPDs
        h += '<table align="center" cellspacing="0" cellpadding="1" border="0" style="border-color:#6fa527;border-width:1px;border-style:ridge;width:786px;border-collapse:collapse;">'
        h += '<tr>'
        h += '<td  align="left" colspan="3" style="font-weight:bold;color:White;background-color:#6fa527;border-color:#6fa527;border-width:2px;border-style:ridge;">'
        h += 'EPDs: ' + title
        h += '</td>'
        h += create_epds_html_row(animal.getAnimalId())
        h += '</table>'
        h += '&nbsp;'
        # h += '<p style="page-break-before:always">'

        # Treatments
        h += '<table align="center" cellspacing="0" cellpadding="1" border="0" style="border-color:#6fa527;border-width:1px;border-style:ridge;width:786px;border-collapse:collapse;">'
        h += '<tr>'
        h += '<td  align="left" colspan="4" style="font-weight:bold;color:White;background-color:#6fa527;border-color:#6fa527;border-width:2px;border-style:ridge;">'
        h += 'Treatments: ' + title
        h += '</td>'
        h += create_treatment_html_row(animal.getAnimalId())
        h += '</table>'
        h += '&nbsp;'

        return (h)

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def find_epds(_id):
    con = None
    SQL_QUERY = _sql.SQL_SELECT_EPDS + " AND e.animal_id = " + str(_id)

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(SQL_QUERY)
        rows = cur.fetchall()
        epds = []

        for row in rows:
            epd = EPD()
            epd.id = str_util.to_pos_int_or_none(row[0])
            epd.animal_id = str_util.to_pos_int_or_none(row[1])
            epd.epd_reporting_period = str_util.to_upper_or_none(row[2])
            epd.epd_type = str_util.to_upper_or_none(row[3])
            epd.ced_epd = str_util.to_float_or_none(row[4])
            epd.ced_acc = str_util.to_float_or_none(row[5])
            epd.bw_epd = str_util.to_float_or_none(row[6])
            epd.bw_acc = str_util.to_float_or_none(row[7])
            epd.ww_epd = str_util.to_float_or_none(row[8])
            epd.ww_acc = str_util.to_float_or_none(row[9])
            epd.yw_epd = str_util.to_float_or_none(row[10])
            epd.yw_acc = str_util.to_float_or_none(row[11])
            epd.milk_epd = str_util.to_float_or_none(row[12])
            epd.milk_acc = str_util.to_float_or_none(row[13])
            epd.mww_epd = str_util.to_float_or_none(row[14])
            epd.mww_acc = str_util.to_float_or_none(row[15])
            epds.append(epd)
        con.commit()
        return (epds)

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def create_measurements_html_row(_eartag):
    con = None
    SQL_SELECT_MEASUREMENTS = "SELECT " \
                              "m.category," \
                              "m.measure_date," \
                              "m.age_at_measure," \
                              "m.weight," \
                              "m.adjusted_weight," \
                              "m.adg," \
                              "m.wda," \
                              "m.reference_weight," \
                              "m.gain," \
                              "m.scrotal" \
                              " FROM cattle.animal AS a, cattle.measurements AS m" \
                              " WHERE a.id = m.animal_id AND a.ear_tag = '" + _eartag + "' ORDER BY measure_date DESC;"

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(_sql.SQL_SELECT_MEASUREMENTS)
        rows = cur.fetchall()

        html = ""
        tr_even_style = '<tr align="left" style="background-color:#f2f2f2;padding:8px;">'
        tr_odd_style = '<tr align="left" style="background-color:white;padding:8px;">'
        counter = 0

        for row in rows:
            category = str_util.to_upper_or_none(row[0])
            measure_date = str_util.to_date_or_none(row[1])
            age_at_measure = str_util.to_pos_int_or_none(row[2])
            weight = str_util.to_pos_int_or_none(row[3])
            adjusted_weight = str_util.to_pos_int_or_none(row[4])
            adg = str_util.to_float_or_none(row[5])
            wda = str_util.to_float_or_none(row[6])
            reference_weight = str_util.to_pos_int_or_none(row[7])
            gain = str_util.to_pos_int_or_none(row[8])
            scrotal = str_util.to_float_or_none(row[9])

            if category == "WORKING WEIGHT":
                continue

            counter += 1

            html_tr = None
            if counter % 2 == 0:
                html_tr = tr_even_style
            else:
                html_tr = tr_odd_style

            if category == 'BIRTH':
                html += html_tr
                html += '<td>' + measure_date.strftime("%b %d, %Y") + '</td>'
                html += '<td>' + str(weight) + ' lbs / ' + str(adjusted_weight) + ' adj</td>'
                html += '<td></td>'
                html += '<td> </td>'
                html += '</tr>'
                html += html_tr
                html += '<td>' + str(category).title() + '</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
            else:
                html += html_tr
                html += '<td>' + measure_date.strftime("%b %d, %Y") + '</td>'
                if adjusted_weight is None:
                    html += '<td>' + str(weight) + ' lbs </td>'
                else:
                    html += '<td>' + str(weight) + ' lbs / ' + str(adjusted_weight) + ' adj</td>'
                html += '<td>' + str(gain) + ' lbs</td>'
                html += '<td> </td>'
                html += '</tr>'
                html += html_tr
                html += '<td>' + str(category).title() + ' - ' + str(age_at_measure) + ' days</td>'
                html += '<td>' + str(wda) + ' lbs/day</td>'
                html += '<td>' + str(adg) + ' lbs/day</td>'
                if scrotal is not None:
                    html += '<td>' + str(round(scrotal, 1)) + ' cm </td>'
                else:
                    html += '<td> </td>'
                html += '</tr>'

        return (html)

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def create_epds_html_row(_animalid):
    con = None
    SQL_SELECT = _sql.SQL_SELECT_EPDS + " AND e.animal_id =" + str(_animalid)

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(SQL_SELECT)
        if cur.rowcount == 0:
            return ""
        rows = cur.fetchall()

        h = ""

        for row in rows:
            epd_reporting_period = str_util.to_upper_or_none(row[2])
            if epd_reporting_period is None:
                return ""
            h += '<tr align="left" style="background-color:#6fa527;color:White;">'
            h += '<td style="text-align:justify;padding:5px;font-weight:bold;">EPD Reporting Period</td>'
            h += '<td colspan="2" >' + epd_reporting_period + '</td>'
            h += '</tr>'
            epd_type = str_util.to_upper_or_none(row[3])
            h += '<tr align="left" style="background-color:#6fa527;color:white;">'
            h += '<td style="text-align:justify;padding:5px;font-weight:bold;">EDP Type</td>'
            h += '<td colspan="2" >' + epd_type + '</td>'
            h += '</tr>'

            h += '<tr align="left" style="color:Black;background-color:#f2f2f2;font-weight: bold;">'
            h += '<td>EPD</td>'
            h += '<td>Value</td>'
            h += '<td>Acc</td>'
            h += '</tr>'

            ced = str_util.to_float_or_none(row[4])
            h += '<tr align="left" style="background-color:white;">'
            h += '<td>Calving Ease Direct</td>'
            h += '<td>' + str(ced) + '</td>'
            ced_acc = str_util.to_float_or_none(row[5])
            if epd_type == "PE" or ced_acc is None:
                h += '<td>PE</td>'
            else:
                h += '<td>' + str(ced_acc) + '</td>'
            h += '</tr>'

            bw_epd = str_util.to_float_or_none(row[6])
            h += '<tr align="left" style="background-color:#f2f2f2;">'
            h += '<td>Birth Weight</td>'
            h += '<td>' + str(bw_epd) + '</td>'
            bw_acc = str_util.to_float_or_none(row[7])
            if epd_type == "PE" or bw_acc is None:
                h += '<td>PE</td>'
            else:
                h += '<td>' + str(bw_acc) + '</td>'
            h += '</tr>'

            ww_epd = str_util.to_float_or_none(row[8])
            h += '<tr align="left" style="background-color:white;">'
            h += '<td>Weaning Weight</td>'
            h += '<td>' + str(ww_epd) + '</td>'
            ww_acc = str_util.to_float_or_none(row[9])
            if epd_type == "PE" or ww_acc is None:
                h += '<td>PE</td>'
            else:
                h += '<td>' + str(ww_acc) + '</td>'
            h += '</tr>'

            yw_epd = str_util.to_float_or_none(row[10])
            h += '<tr align="left" style="background-color:#f2f2f2;">'
            h += '<td>Yearling Weight</td>'
            h += '<td>' + str(yw_epd) + '</td>'
            yw_acc = str_util.to_float_or_none(row[11])
            if epd_type == "PE" or yw_acc is None:
                h += '<td>PE</td>'
            else:
                h += '<td>' + str(yw_acc) + '</td>'
            h += '</tr>'

            milk_epd = str_util.to_float_or_none(row[12])
            h += '<tr align="left" style="background-color:white;">'
            h += '<td>Milk</td>'
            h += '<td>' + str(milk_epd) + '</td>'
            milk_acc = str_util.to_float_or_none(row[13])
            if epd_type == "PE" or milk_acc is None:
                h += '<td>PE</td>'
            else:
                h += '<td>' + str(milk_acc) + '</td>'
            h += '</tr>'

            # mww_epd = str_util.to_float_or_none(row[14])
            # h += '<tr align="left" style="background-color:#f2f2f2;">'
            # h += '<td>Maternal Weaning Weight</td>'
            # h += '<td>' + str(mww_epd) + '</td>'
            # mww_acc = str_util.to_float_or_none(row[15])
            # h += '<td>' + str(mww_acc) + '</td>'
            # h += '</tr>'

        return (h)

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def create_treatment_html_row(_animalid):
    con = None
    sql_select = _sql.SQL_SELECT_TREATMENTS + " AND t.animal_id =" + str(_animalid) + 'ORDER BY t.treatment_date DESC'

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(_sql.SQL_select)
        rows = cur.fetchall()

        tr_even_style = '<tr align="left" style="background-color:#f2f2f2;padding:8px;">'
        tr_odd_style = '<tr align="left" style="background-color:white;padding:8px;">'
        counter = 0

        h = ""
        h += '<tr align="left" style="color:Black;background-color:#f2f2f2;font-weight: bold;">'
        h += '<td>Treatment Date</td>'
        h += '<td>Medication</td>'
        h += '<td></td>'
        h += '<td></td>'
        h += '</tr>'

        for row in rows:
            counter += 1
            html_tr = None
            if counter % 2 == 0:
                html_tr = tr_even_style
            else:
                html_tr = tr_odd_style

            treatment_date = str_util.to_date_or_none(row[2])
            h += html_tr
            if treatment_date is not None:
                h += '<td>' + treatment_date.strftime("%b %d, %Y") + '</td>'
            else:
                h += '<td></td>'
            medication = str_util.to_upper_or_none(row[3])
            if medication == 'FOSGAARD':
                medication = 'FUSOGARD'
            h += '<td colspan="3">' + medication + '</td>'
            h += '</tr>'

        return h

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def create_general_html_row(_animal):
    con = None

    try:
        h = ""
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight:bold;width:100px;">Ear Tag</td>'
        h += '<td colspan="3" style=width:100px;">' + _animal.getEarTag() + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold">Brand</td>'
        h += '<td colspan="3" >' + str(_animal.brand) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Name</td>'
        h += '<td colspan="3" >' + str(_animal.name) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Reg Num</td>'
        h += '<td colspan="3" >' + str(_animal.reg_num) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Electronic ID</td>'
        h += '<td colspan="3" >' + str(_animal.eid) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Animal Type</td>'
        h += '<td colspan="3" >' + str(_animal.animal_type) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Color Markings</td>'
        h += '<td colspan="3" >' + str(_animal.color_markings) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Horn Status</td>'
        h += '<td colspan="3" >' + str(_animal.horn_status) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Breed</td>'
        h += '<td colspan="3" >' + str(_animal.breed) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        date = None
        if _animal.dob is not None:
            date = _animal.dob.strftime("%b %d, %Y")
        h += '<td colspan="1" style="font-weight: bold;">Birth Date</td>'
        h += '<td colspan="3" >' + str(date) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Weaning Date</td>'
        date = None
        if _animal.dow is not None:
            date = _animal.dow.strftime("%b %d, %Y")
        h += '<td colspan="3" >' + str(date) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Yearling Date</td>'
        date = None
        if _animal.doy is not None:
            date = _animal.doy.strftime("%b %d, %Y")
        h += '<td colspan="3" >' + str(date) + '</td>'
        h += '</tr>'
        h += '<tr style="color:black;background-color:white;text-align:left;">'
        h += '<td colspan="1" style="font-weight: bold;">Conception Method</td>'
        h += '<td colspan="3" >' + str(_animal.conception_method) + '</td>'
        h += '</tr>'
        return h

    except psycopg2.DatabaseError as e:
        logging.error(e)

    finally:
        if con:
            con.close()


def sort_tags(_file_name):
    con = None
    csvfile = None
    con = None
    sql_select = SQL_SELECT_ANIMAL + \
                 " LEFT OUTER JOIN cattle.pregnancy_check AS pc ON a.id = pc.animal_id" + \
                 " WHERE pc.check_date = '2016-04-22'"

    try:
        con = psql_util.psql_connection(_database='rafter', _user='postgres', _password='postgres')
        cur = con.cursor()

        cur.execute(_sql.SQL_select)
        rows = cur.fetchall()

        animal_inventory = []

        tag_sort = lambda x: (x[2], x[0], x[1])

        animal_inventory.sort(key=tag_sort)

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                active = str_util.to_upper_or_none(row[25])  # Z

                if active != 'ACTIVE':
                    continue

                id = str_util.to_pos_int_or_none(row[0])  # A
                # sire_id = str_util.to_pos_int_or_none(row[27])  # AB
                # dam_id = str_util.to_pos_int_or_none(row[28])  # AC
                # real_dam_id = str_util.to_pos_int_or_none(row[30])  # AE
                # # breed
                # breed_key = str_util.to_pos_int_or_none(row[20])  # U
                # breed = ec_hashmap.get(breeds, breed_key)
                # breeding_type = ec_hashmap.get(breeding_forms, id)
                # if breeding_type:
                #     if "FLUSH" in breeding_type:
                #         breeding_type = "FLUSH"
                #     elif "AI" in breeding_type:
                #         breeding_type = "AI"
                #     elif "NS" in breeding_type:
                #         breeding_type = "NS"
                #     elif "RECIPIENT" in breeding_type:
                #         breeding_type = "RECIPIENT"
                #     else:
                #         breeding_type = None
                #
                # coat_color_dna = ec_hashmap.get(color_DNAs, id)
                # if coat_color_dna:
                #     if "ED/ED" in coat_color_dna:
                #         coat_color_dna = "ED/ED"
                #     elif "ED/E" in coat_color_dna:
                #         coat_color_dna = "ED/E"
                #     elif "NOT TESTED" in coat_color_dna:
                #         coat_color_dna = "NOT TESTED"
                #     else:
                #         coat_color_dna = None

                ear_tag = str_util.to_upper_or_none(row[3])  # D
                if ear_tag is None:
                    continue

                tag_number = ''
                number_idx = 0
                ear_tag_search = ear_tag
                for i, c in enumerate(ear_tag_search):
                    if i == 0 and c.isdigit():
                        tag_number += c
                    elif c.isdigit() is False:
                        number_idx = i
                        break
                    elif i > 0 and tag_number is not None:
                        tag_number += c

                tag_year = ''
                year_idx = 0
                tag_color = ''

                ear_tag_search = ear_tag[number_idx:]
                for i, c in enumerate(ear_tag_search):
                    if c == '-':
                        tag_color = ear_tag_search[i + 1:]
                        break
                    else:
                        tag_year += c

                tag_list = []
                if tag_number == '':
                    tag_list.append(None)
                else:
                    tag_list.append(int(tag_number))

                tag_list.append(tag_year)
                tag_list.append(tag_color)
                # if tag_color != 'PURPLE':
                #     continue

                animal_inventory.append(tag_list)
                # animal_type = str_util.to_upper_or_none(row[17])
                # sex = str_util.to_upper_or_none(row[18])
                # dob_date = str_util.to_upper_or_none(row[35])
                # dob_year = None
                # if dob_date:
                #     dob_year = dob_date.split("-")[0]
                #
                # seller_id = str_util.to_pos_int_or_none(row[43])  # AR
                # current_breeding_status = str_util.to_upper_or_none(row[59])  # BH
                # last_calving_date = str_util.to_date_or_none(row[58])  # BG
                # estimated_calving_date = str_util.to_date_or_none(row[60])  # BI
                # last_breeding_date = str_util.to_date_or_none(row[58])
                # contact_id = str_util.to_pos_int_or_none(row[43])  # AR
                # dob = str_util.to_date_or_none(row[35])
                #
                # cur.execute(_const.SQL_INSERT_COW, (
                #     id,
                #     active,
                #     sire_id,
                #     dam_id,
                #     real_dam_id,
                #     breed,
                #     breeding_type,
                #     coat_color_dna,
                #     current_breeding_status,
                #     dob,
                #     ear_tag,
                #     estimated_calving_date,
                #     last_breeding_date,
                #     last_calving_date,
                #     contact_id))
                # con.commit()

        animal_inventory.sort(key=tag_sort)

        for tag in animal_inventory:
            ear_tag = str(tag[0]) + str(tag[1]) + '-' + str(tag[2])

    except psycopg2.DatabaseError as e:
        sys.exit(1)

    finally:
        if con:
            con.close()
        if csvfile:
            csvfile.close()


def find_last_worked_cows(_pasture: str, _work_date: str) -> list:
    try:
        animals = Animal.objects(pasture=_pasture, animal_type="COW", sex="HEIFER", status="ACTIVE", treatments__gte={"treatment_date": _work_date})
        return animals

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info(f"{inspect.stack()[0][3]} {'Done.'}")


def match_cm_to_list(_file_name: str) -> list:
    try:
        animals = Animal.objects(animal_type="COW", pasture="LOUISE", sex="HEIFER", status="ACTIVE")

        ear_tags_list = list()
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                ear_tags_list.append(str_util.to_upper_or_none(row[0]))

        ear_tags_not_found = list()
        for animal in animals:
            if animal.ear_tag not in ear_tags_list:
                ear_tags_not_found.append(animal.ear_tag)

        return ear_tags_not_found

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info(f"{inspect.stack()[0][3]} {'Done.'}")



def match_list_to_cm(_file_name: str) -> list:
    try:
        ear_tags = list()

        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for row in reader:
                ear_tag = str_util.to_upper_or_none(row[0])  # B
                # obtain the referenced animal
                animal = Animal.objects(ear_tag=ear_tag).first()
                if not animal:
                    ear_tags.append(ear_tag)

        return ear_tags

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info(f"{inspect.stack()[0][3]} {'Done.'}")


def load_treatments(_file_name: str) -> None:
    try:
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)

            for row in reader:
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                # obtain the referenced animal
                animal = Animal.objects(id=animal_id).first()
                if not animal:
                    continue

                treatment = Treatment()
                treatment.category = str_util.to_upper_or_none(row[5])  # F
                treatment.treatment_date = str_util.to_date_or_none(row[2])  # D
                if not treatment.treatment_date:
                    continue
                treatment.medication = str_util.to_upper_or_none(row[6])  # G
                treatment.dosage = str_util.to_upper_or_none(row[10])  # K
                animal.treatments.append(treatment)
                animal.save()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info(f"{inspect.stack()[0][3]} {'Done.'}")


def load_measurements(_file_name: str) -> None:
    try:
        with open(_file_name, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader, None)

            for row in reader:
                animal_id = str_util.to_pos_int_or_none(row[1])  # B
                # obtain the referenced animal
                animal = Animal.objects(id=animal_id).first()
                if not animal:
                    continue

                measure = Measurement()
                category = str_util.to_upper_or_none(row[2])  # C
                if category not in Measurement.MEASUREMENT_CATEGORY:
                    continue
                measure.category = category
                measure.measure_date = str_util.to_date_or_none(row[3])  # D
                if not measure.measure_date:
                    continue
                measure.age_at_measure = str_util.to_pos_int_or_none(row[4])  # E
                measure.weight = str_util.to_pos_int_or_none(row[5])
                measure.adjusted_weight = str_util.to_pos_int_or_none(row[6])
                measure.adg = str_util.to_float_or_none(row[8])
                measure.wda = str_util.to_float_or_none(row[10])
                measure.scrotal = str_util.to_float_or_none(row[16])
                measure.reference_date = str_util.to_date_or_none(row[18])
                measure.reference_weight = str_util.to_pos_int_or_none(row[19])
                measure.gain = str_util.to_pos_int_or_none(row[20])
                animal.measurements.append(measure)
                animal.save()

    except Exception as e:
        logging.error("{} {}".format(inspect.stack()[0][3], e))

    finally:
        logging.info(f"{inspect.stack()[0][3]} {'Done.'}")
