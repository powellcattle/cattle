from typing import List

from nosql.animal import Animal


def find_by_ear_tag(ear_tag: str) -> Animal:
    """

    Will return the first Animal with the supplied ear tag value

    :param ear_tag:  An animal ear tag
    :return: Animal
    """
    return Animal.objects(ear_tag=ear_tag.upper()).first()


def like_ear_tag(search_pattern: str, animal_type=None, return_limit=10) -> List[Animal]:
    """

    Find all animals with an ear tag that contains any or all of the supplied ear tag pattern

    :param search_pattern:  Supplied ear tag search pattern
    :param animal_type:  Restricts the search to the animal type, with the default to None which will not restrict and will look for COW, CALF, and BULL
    :param return_limit:  Determines the number of results returned
    :return: List[Animal]
    """
    if animal_type:
        return Animal.objects(ear_tag__contains=search_pattern.upper(), animal_type=animal_type.upper())[:return_limit]
    else:
        return Animal.objects(ear_tag__contains=search_pattern.upper())[:return_limit]
