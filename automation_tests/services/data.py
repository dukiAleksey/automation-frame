import string
import random
import hashlib

from datetime import datetime, timedelta
from time import sleep

from constants.api.abc_api import Host
from constants.abc_api import CustomerId
from constants.api.tsm import Languages as Lang


def get_random_int(low=1000, top=10000):
    return random.randint(low, top)


def get_random_string(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def get_random_text(size_from=1, size_to=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    size = random.choice(range(size_from, size_to + 1))
    space_position = random.choice(range(1, 10))
    res_text = ''
    for i in range(size):
        if i == space_position:
            res_text += ' '
            space_position += random.choice(range(1, 10))
        else:
            res_text += random.choice(chars)
    return res_text


def get_random_email(size=10):
    return f"{get_random_string(size=size, chars=string.ascii_lowercase+string.digits)}@test.com"


def get_md5_password(passw=get_random_string(12)):
    md5 = hashlib.md5()
    md5.update(passw.encode('utf-8'))
    return md5.hexdigest()


def get_random_lang():
    return random.choice(["en-US", "fr-FR"])


def get_random_country(alpha=2):
    if alpha == 3:
        return random.choice(['FRA', 'FRO', 'FSM', 'GAB', 'GBR', 'GEO', 'GGY', 'GHA', 'GIB', 'GIN', 'GLP', 'GMB'])
    else:
        return random.choice(["BE", "GB", "FR", "RU", "LT", "JP", "PL", "BY"])


def get_random_product_category():
    return random.choice([{"name": "Add-on", "category_id": 7},
                          {"name": "Top-up", "category_id": 2},
                          {"name": "Recurring", "category_id": 10},
                          {"name": "One-off", "category_id": 9}])


def get_random_channel():
    return random.choice([{"value": "SFC", "id": 286},
                          {"value": "SFC_APP", "id": 287},
                          {"value": "SFC_WEB", "id": 288}])


def get_random_status():
    return random.choice(["ALIVE", "HISTORY"])


def get_random_source():
    return random.choice(["SFC_APP", "SFC_WEB"])


def get_random_brand(current_brand=None):
    possible_brands = ["Alfa Romeo", "Maserati", "Jeep"]
    if current_brand:
        possible_brands.remove(current_brand)
        return random.choice(possible_brands)
    return random.choice(possible_brands)


def get_date(future=True, days=None, minutes=None):
    if future:
        if minutes:
            return (datetime.utcnow() + timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        elif days:
            return (datetime.utcnow() + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        if minutes:
            return (datetime.utcnow() - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        elif days:
            return (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def get_lang_by_id(_id):
    if _id == 1:
        return Lang.EN
    elif _id == 2:
        return Lang.FR
    elif _id == 3:
        return Lang.NL
    elif _id == 4:
        return Lang.JP
    elif _id == 5:
        return Lang.CN
    elif _id == 6:
        return Lang.IT
    elif _id == 7:
        return Lang.DE
    elif _id == 15:
        return Lang.ES
    elif _id == 25:
        return Lang.PT
    else:
        raise Exception("No one language doesn't match to language_id")
