
from nosql import query, mongo_setup

mongo_setup.global_init()




animals = query.like_ear_tag("MAIN 68B")
for animal in animals:
    print(f"{animal.ear_tag}")
    if animal.dam_animal:
        print(f"\t{animal.dam_animal.ear_tag}")
    if animal.sire_animal:
        print(f"\t{animal.sire_animal.ear_tag}")

    for os in animal.offspring:
        if os.ear_tag:
            print(f"\t\t{os.ear_tag}")





# animal = query.find_by_ear_tag("326a-white")
#
#
# print(f"S:{animal.sire_animal.ear_tag}")
# print(f"D:{animal.dam_animal.ear_tag}")
# if animal.preg_check:
#     print(f"\t|-->{animal.ear_tag} {animal.preg_check.result}")
# else:
#     print(f"\t|-->{animal.ear_tag}")
# for animal in animal.offspring:
#
#         print(f"\t\t|-->{animal.ear_tag}")
# animal = query.find_by_ear_tag("16D-WHITE")
#
# print(f"S:{animal.sire_animal.ear_tag}")
# print(f"D:{animal.dam_animal.ear_tag}")
# if animal.preg_check:
#     print(f"\t|-->{animal.ear_tag} {animal.preg_check.result}")
# else:
#     print(f"\t|-->{animal.ear_tag}")
# for animal in animal.offspring:
#     print(f"\t\t|-->{animal.ear_tag}")