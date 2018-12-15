SQL_INSERT_CONTACT = "INSERT INTO cattle.contact(" \
                     "id," \
                     "name)" \
                     "VALUES (%s,%s)"
SQL_DROP_CONTACT = "DROP TABLE IF EXISTS cattle.contact CASCADE"
SQL_CREATE_CONTACT = "CREATE TABLE cattle.contact(" \
                     "id integer NOT NULL," \
                     "name character varying(50) NOT NULL," \
                     "CONSTRAINT cattle_contact_pkey PRIMARY KEY (id))"


SQL_INSERT_BULL = "INSERT INTO cattle.bull(" \
                  "id," \
                  "sire_id," \
                  "dam_id," \
                  "real_dam_id," \
                  "breed, " \
                  "breeding_type, " \
                  "coat_color_dna, " \
                  "current_breeding_status," \
                  "dob, " \
                  "ear_tag, " \
                  "contact_id)" \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_BULL = "DROP TABLE IF EXISTS cattle.bull CASCADE"
SQL_CREATE_BULL = "CREATE TABLE cattle.bull(" \
                  "id integer NOT NULL," \
                  "sire_id integer," \
                  "dam_id integer," \
                  "real_dam_id integer," \
                  "breed character varying(20)," \
                  "breeding_type character varying(10)," \
                  "coat_color_dna character varying(10)," \
                  "current_breeding_status character varying(10)," \
                  "dob date," \
                  "ear_tag character varying(50)," \
                  "contact_id integer," \
                  "CONSTRAINT bull_pkey PRIMARY KEY (id))"

SQL_INSERT_CALF = "INSERT INTO cattle.calf(" \
                  "id," \
                  "sire_id," \
                  "dam_id," \
                  "real_dam_id," \
                  "sex," \
                  "breed," \
                  "coat_color_dna," \
                  "dob," \
                  "ear_tag," \
                  "birth_weight," \
                  "weaning_weight," \
                  "yearling_weight," \
                  "adj_birth_weight," \
                  "adj_weaning_weight," \
                  "adj_yearling_weight)" \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_CALF = "DROP TABLE IF EXISTS cattle.calf CASCADE"
SQL_CREATE_CALF = "CREATE TABLE cattle.calf(" \
                  "id integer NOT NULL," \
                  "sire_id integer," \
                  "dam_id integer," \
                  "real_dam_id integer," \
                  "sex character varying(10)," \
                  "breed character varying(20)," \
                  "coat_color_dna character varying(10)," \
                  "dob date," \
                  "ear_tag character varying(50) NOT NULL," \
                  "birth_weight integer," \
                  "weaning_weight integer," \
                  "yearling_weight integer," \
                  "adj_birth_weight integer," \
                  "adj_weaning_weight integer," \
                  "adj_yearling_weight integer," \
                  "CONSTRAINT calf_pkey PRIMARY KEY (id))"

SQL_INSERT_BREED_COMPOSITIONS = "INSERT INTO cattle.breed_compositions(" \
                                "id," \
                                "animal_id," \
                                "breed_id," \
                                "percentage)" \
                                "VALUES (%s,%s,%s,%s)"
SQL_DROP_BREED_COMPOSITIONS = "DROP TABLE IF EXISTS cattle.breed_compositions CASCADE"
SQL_CREATE_BREED_COMPOSITIONS = "CREATE TABLE cattle.breed_compositions(" \
                                "id INTEGER NOT NULL," \
                                "animal_id INTEGER NOT NULL," \
                                "breed_id INTEGER NOT NULL," \
                                "percentage INTEGER," \
                                "CONSTRAINT cattle_breed_compositions_pkey PRIMARY KEY (id))"

SQL_INSERT_BREEDS = "INSERT INTO cattle.breeds(" \
                    "id," \
                    "name," \
                    "gestation_period," \
                    "breed_association_id) " \
                    "VALUES (%s,%s,%s,%s)"
SQL_DROP_BREEDS = "DROP TABLE IF EXISTS cattle.breeds CASCADE"
SQL_CREATE_BREEDS = "CREATE TABLE cattle.breeds(" \
                    "id INTEGER NOT NULL," \
                    "name VARCHAR(30) NOT NULL," \
                    "gestation_period INTEGER NOT NULL," \
                    "breed_association_id INTEGER," \
                    "CONSTRAINT cattle_breeds_pkey PRIMARY KEY (id))"

SQL_INSERT_COW = "INSERT INTO cattle.cow(" \
                 "id," \
                 "active," \
                 "sire_id," \
                 "dam_id," \
                 "real_dam_id," \
                 "breed, " \
                 "breeding_type, " \
                 "coat_color_dna, " \
                 "current_breeding_status," \
                 "dob, " \
                 "ear_tag, " \
                 "estimated_calving_date, " \
                 "last_breeding_date, " \
                 "last_calving_date," \
                 "contact_id)" \
                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_COW = "DROP TABLE IF EXISTS cattle.cow CASCADE"
SQL_CREATE_COW = "CREATE TABLE cattle.cow(" \
                 "id integer NOT NULL," \
                 "active character varying(20)," \
                 "sire_id integer," \
                 "dam_id integer," \
                 "real_dam_id integer," \
                 "breed character varying(20)," \
                 "breeding_type character varying(10)," \
                 "coat_color_dna character varying(10)," \
                 "current_breeding_status character varying(10)," \
                 "dob date," \
                 "ear_tag character varying(50)," \
                 "estimated_calving_date date," \
                 "last_breeding_date date," \
                 "last_calving_date date," \
                 "contact_id integer," \
                 "CONSTRAINT cow_pkey PRIMARY KEY (id))"

SQL_INSERT_BREEDING = "INSERT INTO cattle.breeding(" \
                      "id," \
                      "animal_id," \
                      "bull_animal_id," \
                      "breeding_method," \
                      "breeding_date," \
                      "breeding_end_date," \
                      "estimated_calving_date," \
                      "cleanup," \
                      "embryo_id," \
                      "pregnancy_check_id)" \
                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_BREEDING = "DROP TABLE cattle.breeding CASCADE"
SQL_CREATE_BREEDING = "CREATE TABLE cattle.breeding(" \
                      "id integer NOT NULL," \
                      "animal_id integer NOT NULL," \
                      "bull_animal_id integer," \
                      "breeding_method character(2)," \
                      "breeding_date date NOT NULL," \
                      "breeding_end_date date," \
                      "estimated_calving_date date," \
                      "cleanup boolean NOT NULL," \
                      "embryo_id integer," \
                      "pregnancy_check_id integer," \
                      "CONSTRAINT breeding_pkey PRIMARY KEY (id))"

SQL_INSERT_CONTACT = "INSERT INTO cattle.contact(" \
                     "id," \
                     "name)" \
                     "VALUES (%s,%s)"
SQL_DROP_CONTACT = "DROP TABLE IF EXISTS cattle.contact CASCADE"
SQL_CREATE_CONTACT = "CREATE TABLE cattle.contact(" \
                     "id integer NOT NULL," \
                     "name character varying(50) NOT NULL," \
                     "CONSTRAINT cattle_contact_pkey PRIMARY KEY (id))"

SQL_INSERT_PASTURE = "INSERT INTO cattle.pasture(" \
                     "id," \
                     "acres," \
                     "animal_count," \
                     "name)" \
                     "VALUES (%s,%s,%s,%s)"
SQL_DROP_PASTURE = "DROP TABLE IF EXISTS cattle.pasture CASCADE"
SQL_CREATE_PASTURE = "CREATE TABLE cattle.pasture(" \
                     "id integer NOT NULL," \
                     "acres FLOAT," \
                     "animal_count integer NOT NULL," \
                     "name character varying(50) NOT NULL," \
                     "CONSTRAINT cattle_pasture_pkey PRIMARY KEY (id))"

SQL_INSERT_TREATMENTS = "INSERT INTO cattle.treatments(" \
                        "id," \
                        "animal_id," \
                        "treatment_date," \
                        "medication) " \
                        "VALUES (%s,%s,%s,%s)"
SQL_DROP_TREATMENTS = "DROP TABLE IF EXISTS cattle.treatments CASCADE"
SQL_CREATE_TREATMENTS = "CREATE TABLE cattle.treatments(" \
                        "id INTEGER NOT NULL," \
                        "animal_id INTEGER NOT NULL," \
                        "treatment_date DATE," \
                        "medication VARCHAR(30)," \
                        "CONSTRAINT cattle_treatment_pkey PRIMARY KEY (id))"

SQL_SELECT_TREATMENTS = "SELECT " \
                        "t.id," \
                        "t.animal_id," \
                        "t.treatment_date," \
                        "t.medication " \
                        "FROM cattle.treatments AS t, cattle.animal a " \
                        "WHERE a.id = t.animal_id "


SQL_INSERT_EPDS = "INSERT INTO cattle.epds(" \
                  "id," \
                  "animal_id," \
                  "epd_reporting_period," \
                  "epd_type," \
                  "ced_epd," \
                  "ced_acc," \
                  "bw_epd," \
                  "bw_acc," \
                  "ww_epd," \
                  "ww_acc," \
                  "yw_epd," \
                  "yw_acc," \
                  "milk_epd," \
                  "milk_acc, " \
                  "mww_epd," \
                  "mww_acc) " \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_EPDS = "DROP TABLE IF EXISTS cattle.epds CASCADE"
SQL_CREATE_EPDS = "CREATE TABLE cattle.epds(" \
                  "id INTEGER NOT NULL," \
                  "animal_id INTEGER NOT NULL," \
                  "epd_reporting_period VARCHAR(20)," \
                  "epd_type VARCHAR(20)," \
                  "ced_epd FLOAT," \
                  "ced_acc FLOAT," \
                  "bw_epd FLOAT," \
                  "bw_acc FLOAT," \
                  "ww_epd FLOAT," \
                  "ww_acc FLOAT," \
                  "yw_epd FLOAT," \
                  "yw_acc FLOAT," \
                  "milk_epd FLOAT," \
                  "milk_acc FLOAT," \
                  "mww_epd FLOAT," \
                  "mww_acc FLOAT," \
                  "CONSTRAINT cattle_epds_pkey PRIMARY KEY (id))"

SQL_SELECT_EPDS = "SELECT " \
                  "e.id," \
                  "e.animal_id," \
                  "e.epd_reporting_period," \
                  "e.epd_type," \
                  "e.ced_epd," \
                  "e.ced_acc," \
                  "e.bw_epd," \
                  "e.bw_acc," \
                  "e.ww_epd," \
                  "e.ww_acc," \
                  "e.yw_epd," \
                  "e.yw_acc," \
                  "e.milk_epd," \
                  "e.milk_acc," \
                  "e.mww_epd," \
                  "e.mww_acc " \
                  "FROM cattle.epds AS e, cattle.animal a " \
                  "WHERE a.id = e.animal_id "


class EPD(object):
    def __init__(self):
        self.id = None
        self.animal_id = None
        self.epd_reporting_period = None
        self.epd_type = None
        self.ced_epd = None
        self.ced_acc = None
        self.bw_epd = None
        self.bw_acc = None
        self.ww_epd = None
        self.ww_acc = None
        self.yw_epd = None
        self.yw_acc = None
        self.milk_epd = None
        self.milk_acc = None
        self.mww_epd = None
        self.mww_acc = None


SQL_SELECT_ANIMAL = "SELECT " \
                    "a.id," \
                    "a.ear_tag," \
                    "a.ear_tag_loc," \
                    "a.tattoo_left," \
                    "a.tattoo_right," \
                    "a.brand," \
                    "a.brand_loc," \
                    "a.name," \
                    "a.reg_num," \
                    "a.reg_num_2," \
                    "a.other_id," \
                    "a.other_id_loc," \
                    "a.electronic_id," \
                    "a.animal_type," \
                    "a.sex," \
                    "a.breed_id," \
                    "a.horn_status," \
                    "a.color_markings," \
                    "a.ocv_tattoo," \
                    "a.ocv_number," \
                    "a.status," \
                    "a.pasture_id," \
                    "a.sire_animal_id," \
                    "a.dam_animal_id," \
                    "a.genetic_dam_animal_id," \
                    "a.real_dam_animal_id," \
                    "a.sire_legacy_id," \
                    "a.dam_legacy_id," \
                    "a.genetic_dam_legacy_id," \
                    "a.breeder_contact_id," \
                    "a.birth_date," \
                    "a.birth_year," \
                    "a.weaning_date," \
                    "a.yearling_date," \
                    "a.percent_dam_weight," \
                    "a.conception_method," \
                    "a.grafted_calf," \
                    "a.purchase_date," \
                    "a.purchased," \
                    "a.purchased_from_contact_id," \
                    "a.purchase_price," \
                    "a.sale_ticket_id," \
                    "a.sale_price," \
                    "a.sale_weight," \
                    "a.marketing_cost," \
                    "a.reason_for_sale," \
                    "a.death_date," \
                    "a.cause_of_death," \
                    "a.asking_price," \
                    "a.marketing_comments," \
                    "a.mppa," \
                    "a.avg_calving_interval," \
                    "a.avg_post_partum_interval," \
                    "a.last_breeding_date," \
                    "a.last_calving_date," \
                    "a.current_breeding_status," \
                    "a.next_calving_date," \
                    "a.pelvic_area," \
                    "a.pelvic_horizontal," \
                    "a.pelvic_vertical," \
                    "a.comments," \
                    "a.donor_cow," \
                    "a.ai_bull," \
                    "a.promote_date," \
                    "a.demote_date," \
                    "a.birth_weight," \
                    "a.weaning_weight," \
                    "a.yearling_weight," \
                    "a.adj_birth_weight," \
                    "a.adj_weaning_weight," \
                    "a.adj_yearling_weight," \
                    "a.last_tip_to_tip," \
                    "a.last_total_horn," \
                    "a.last_base," \
                    "a.last_composite," \
                    "a.last_horn_measure_date," \
                    "a.last_weight," \
                    "a.last_height," \
                    "a.last_bcs," \
                    "a.last_weight_date," \
                    "a.embryo_recovery_date," \
                    "a.nait_number," \
                    "a.nlis_number," \
                    "a.last_treatment_date," \
                    "a.withdrawal_date," \
                    "a.castration_date," \
                    "a.next_booster_date," \
                    "b.name," \
                    "bc.percentage " \
                    "FROM cattle.animal AS a "

SQL_INSERT_EMBRYOS = "INSERT INTO cattle.embryos(" \
                     "id," \
                     "sire_id," \
                     "dam_id)" \
                     "VALUES (%s,%s,%s)"
SQL_DROP_EMBRYOS = "DROP TABLE IF EXISTS cattle.embryos CASCADE"
SQL_CREATE_EMBRYOS = "CREATE TABLE cattle.embryos(" \
                     "id integer NOT NULL," \
                     "sire_id integer NOT NULL," \
                     "dam_id integer NOT NULL," \
                     "CONSTRAINT cattle_embryos_pkey PRIMARY KEY (id))"

SQL_INSERT_MOVEMENTS = "INSERT INTO cattle.movements(" \
                       "id," \
                       "animal_id," \
                       "moved_from_pasture_id," \
                       "moved_to_pasture_id," \
                       "movement_date)" \
                       "VALUES (%s,%s,%s,%s,%s)"
SQL_DROP_MOVEMENTS = "DROP TABLE IF EXISTS cattle.movements CASCADE"
SQL_CREATE_MOVEMENTS = "CREATE TABLE cattle.movements(" \
                       "id integer NOT NULL," \
                       "animal_id integer NOT NULL," \
                       "moved_from_pasture_id integer," \
                       "moved_to_pasture_id integer," \
                       "movement_date date," \
                       "CONSTRAINT cattle_movement_pkey PRIMARY KEY (id))"

SQL_TRUE_TEST = "SELECT " \
                "a.ear_tag AS VID," \
                "a.electronic_id AS EID," \
                "b.name AS BREED," \
                "a.brand AS LID," \
                "a.animal_type AS TYPE," \
                "a.color_markings AS COLOR," \
                "a.sex as SEX " \
                "FROM cattle.animal AS a, cattle.breeds AS b " \
                "WHERE a.breed_id = b.id AND a.status = 'ACTIVE' AND a.ear_tag NOT LIKE '%NEED%'"

SQL_SELECT_ALLFLEX = "SELECT " \
                     "a.ear_tag AS VID," \
                     "a.electronic_id AS EID," \
                     "b.name AS BREED," \
                     "a.brand AS LID," \
                     "a.animal_type AS TYPE," \
                     "a.color_markings AS COLOR," \
                     "a.sex as SEX, " \
                     "a.horn_status AS HORN_STATUS " \
                     "FROM cattle.animal AS a, cattle.breeds AS b " \
                     "WHERE a.breed_id = b.id AND a.status = 'ACTIVE' AND a.electronic_id IS NOT NULL AND a.ear_tag NOT LIKE '%NEED%'"

SQL_INSERT_MEASUREMENTS = "INSERT INTO cattle.measurements(" \
                          "id," \
                          "animal_id," \
                          "category," \
                          "measure_date," \
                          "age_at_measure," \
                          "weight," \
                          "adjusted_weight," \
                          "adg," \
                          "wda," \
                          "reference_weight," \
                          "gain," \
                          "scrotal)" \
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_MEASUREMENTS = "DROP TABLE IF EXISTS cattle.measurements CASCADE"
SQL_CREATE_MEASUREMENTS = "CREATE TABLE cattle.measurements(" \
                          "id INTEGER NOT NULL," \
                          "animal_id INTEGER NOT NULL," \
                          "category VARCHAR(20)," \
                          "measure_date DATE," \
                          "age_at_measure INTEGER," \
                          "weight INTEGER," \
                          "adjusted_weight INTEGER," \
                          "adg FLOAT," \
                          "wda FLOAT," \
                          "reference_weight INTEGER," \
                          "gain INTEGER," \
                          "scrotal FLOAT," \
                          "CONSTRAINT cattle_measurements_pkey PRIMARY KEY (id))"
SQL_INSERT_ANIMAL = "INSERT INTO cattle.animal(" \
                    "id," \
                    "ear_tag," \
                    "ear_tag_prefix," \
                    "ear_tag_year_desig," \
                    "ear_tag_color," \
                    "ear_tag_loc," \
                    "tattoo_left," \
                    "tattoo_right," \
                    "brand," \
                    "brand_loc," \
                    "name," \
                    "reg_num," \
                    "reg_num_2," \
                    "other_id," \
                    "other_id_loc," \
                    "electronic_id," \
                    "animal_type," \
                    "sex," \
                    "breed_id," \
                    "horn_status," \
                    "color_markings," \
                    "ocv_tattoo," \
                    "ocv_number," \
                    "status," \
                    "pasture_id," \
                    "sire_animal_id," \
                    "dam_animal_id," \
                    "genetic_dam_animal_id," \
                    "real_dam_animal_id," \
                    "sire_legacy_id," \
                    "dam_legacy_id," \
                    "genetic_dam_legacy_id," \
                    "breeder_contact_id," \
                    "birth_date," \
                    "birth_year," \
                    "weaning_date," \
                    "yearling_date," \
                    "percent_dam_weight," \
                    "conception_method," \
                    "grafted_calf," \
                    "purchase_date," \
                    "purchased," \
                    "purchased_from_contact_id," \
                    "purchase_price," \
                    "sale_ticket_id," \
                    "sale_price," \
                    "sale_weight," \
                    "marketing_cost," \
                    "reason_for_sale," \
                    "death_date," \
                    "cause_of_death," \
                    "asking_price," \
                    "marketing_comments," \
                    "mppa," \
                    "avg_calving_interval," \
                    "avg_post_partum_interval," \
                    "last_breeding_date," \
                    "last_calving_date," \
                    "current_breeding_status," \
                    "next_calving_date," \
                    "pelvic_area," \
                    "pelvic_horizontal," \
                    "pelvic_vertical," \
                    "comments," \
                    "donor_cow," \
                    "ai_bull," \
                    "promote_date," \
                    "demote_date," \
                    "birth_weight," \
                    "weaning_weight," \
                    "yearling_weight," \
                    "adj_birth_weight," \
                    "adj_weaning_weight," \
                    "adj_yearling_weight," \
                    "last_tip_to_tip," \
                    "last_total_horn," \
                    "last_base," \
                    "last_composite," \
                    "last_horn_measure_date," \
                    "last_weight," \
                    "last_height," \
                    "last_bcs," \
                    "last_weight_date," \
                    "embryo_recovery_date," \
                    "nait_number," \
                    "nlis_number," \
                    "last_treatment_date," \
                    "withdrawal_date," \
                    "castration_date," \
                    "next_booster_date) " \
                    "VALUES (" \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

SQL_DROP_ANIMAL = "DROP TABLE IF EXISTS cattle.animal CASCADE"
SQL_CREATE_ANIMAL = "CREATE TABLE cattle.animal(" \
                    "id INTEGER NOT NULL," \
                    "ear_tag VARCHAR(50)," \
                    "ear_tag_prefix INTEGER," \
                    "ear_tag_year_desig VARCHAR(10)," \
                    "ear_tag_color VARCHAR(50)," \
                    "ear_tag_loc VARCHAR(2)," \
                    "tattoo_left VARCHAR(25)," \
                    "tattoo_right VARCHAR(25)," \
                    "brand VARCHAR(25)," \
                    "brand_loc VARCHAR(2)," \
                    "name VARCHAR(50)," \
                    "reg_num VARCHAR(25)," \
                    "reg_num_2 VARCHAR(25)," \
                    "other_id VARCHAR(25)," \
                    "other_id_loc VARCHAR(25)," \
                    "electronic_id VARCHAR(25)," \
                    "animal_type VARCHAR(10) NOT NULL," \
                    "sex VARCHAR(6)," \
                    "breed_id INTEGER," \
                    "horn_status VARCHAR(12)," \
                    "color_markings VARCHAR(50)," \
                    "ocv_tattoo VARCHAR(25)," \
                    "ocv_number VARCHAR(25)," \
                    "status VARCHAR(9)," \
                    "pasture_id INTEGER," \
                    "sire_animal_id INTEGER," \
                    "dam_animal_id INTEGER," \
                    "genetic_dam_animal_id INTEGER," \
                    "real_dam_animal_id INTEGER," \
                    "sire_legacy_id INTEGER," \
                    "dam_legacy_id INTEGER," \
                    "genetic_dam_legacy_id INTEGER," \
                    "breeder_contact_id INTEGER," \
                    "birth_date DATE," \
                    "birth_year INTEGER," \
                    "weaning_date DATE," \
                    "yearling_date DATE," \
                    "percent_dam_weight REAL," \
                    "conception_method VARCHAR(2)," \
                    "grafted_calf BOOLEAN," \
                    "purchase_date DATE," \
                    "purchased BOOLEAN," \
                    "purchased_from_contact_id INTEGER," \
                    "purchase_price REAL," \
                    "sale_ticket_id INTEGER," \
                    "sale_price REAL," \
                    "sale_weight REAL," \
                    "marketing_cost REAL," \
                    "reason_for_sale VARCHAR(100)," \
                    "death_date DATE," \
                    "cause_of_death VARCHAR(50)," \
                    "asking_price REAL," \
                    "marketing_comments VARCHAR(100)," \
                    "mppa REAL," \
                    "avg_calving_interval INTEGER," \
                    "avg_post_partum_interval INTEGER," \
                    "last_breeding_date DATE," \
                    "last_calving_date DATE," \
                    "current_breeding_status VARCHAR(20)," \
                    "next_calving_date DATE," \
                    "pelvic_area REAL," \
                    "pelvic_horizontal REAL," \
                    "pelvic_vertical REAL," \
                    "comments VARCHAR(100)," \
                    "donor_cow BOOLEAN," \
                    "ai_bull BOOLEAN," \
                    "promote_date DATE," \
                    "demote_date DATE," \
                    "birth_weight REAL," \
                    "weaning_weight REAL," \
                    "yearling_weight REAL," \
                    "adj_birth_weight REAL," \
                    "adj_weaning_weight REAL," \
                    "adj_yearling_weight REAL," \
                    "last_tip_to_tip REAL," \
                    "last_total_horn REAL," \
                    "last_base REAL," \
                    "last_composite REAL," \
                    "last_horn_measure_date REAL," \
                    "last_weight INTEGER," \
                    "last_height INTEGER," \
                    "last_bcs INTEGER," \
                    "last_weight_date DATE," \
                    "embryo_recovery_date DATE," \
                    "nait_number INTEGER," \
                    "nlis_number INTEGER," \
                    "last_treatment_date DATE," \
                    "withdrawal_date DATE," \
                    "castration_date DATE," \
                    "next_booster_date DATE," \
                    "CONSTRAINT animal_pkey PRIMARY KEY (id))"

SQL_INSERT_BREEDING = "INSERT INTO cattle.breeding(" \
                      "id," \
                      "animal_id, " \
                      "bull_animal_id, " \
                      "breeding_method, " \
                      "breeding_date," \
                      "breeding_end_date, " \
                      "estimated_calving_date, " \
                      "cleanup, " \
                      "embryo_id," \
                      "pregnancy_check_id)" \
                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_BREEDING = "DROP TABLE IF EXISTS cattle.breeding CASCADE"
SQL_CREATE_BREEDING = "CREATE TABLE cattle.breeding (" \
                      "id integer NOT NULL," \
                      "animal_id integer NOT NULL," \
                      "bull_animal_id integer," \
                      "breeding_method character(2)," \
                      "breeding_date date NOT NULL," \
                      "breeding_end_date date," \
                      "estimated_calving_date date," \
                      "cleanup boolean NOT NULL," \
                      "embryo_id integer," \
                      "pregnancy_check_id integer," \
                      "CONSTRAINT breeding_pkey PRIMARY KEY (id))"

SQL_INSERT_PREG = "INSERT INTO cattle.pregnancy_check(" \
                  "id," \
                  "animal_id," \
                  "check_date," \
                  "check_method," \
                  "result," \
                  "ultrasound_sex," \
                  "expected_due_date)" \
                  "VALUES (%s,%s,%s,%s,%s,%s,%s)"
SQL_DROP_PREG = "DROP TABLE IF EXISTS cattle.pregnancy_check CASCADE"
SQL_CREATE_PREG = "CREATE TABLE cattle.pregnancy_check(" \
                  "id integer NOT NULL," \
                  "animal_id integer NOT NULL," \
                  "check_date date NOT NULL," \
                  "check_method character varying(12) NOT NULL," \
                  "result character varying(10) NOT NULL," \
                  "ultrasound_sex character varying(8)," \
                  "expected_due_date date," \
                  "CONSTRAINT pregnancy_check_pkey PRIMARY KEY (id))"