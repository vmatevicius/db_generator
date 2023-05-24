from typing import Dict, List, Optional, Union
import random
from py_random_words import RandomWords
from datetime import timezone, datetime, timedelta
def get_database_name() -> str:
    return input("Enter database name: ")


def get_collection_name() -> str:
    return input("Enter collection name: ")


def create_empty_document() -> Dict:
    document = {}
    while True:
        name = get_field_name()
        document[name] = make_field_value_template()
        if handle_yes_no_inputs():
            continue
        else:
            break
    return document


def handle_yes_no_inputs():
    while True:
        response = input("Do you want to continue? (y/n): ").strip().lower()
        if response not in ["y", "n"]:
            print("Wrong input")
            continue
        else:
            break
    if response == "y":
        return True
    return False


def get_field_name() -> str:
    return input("Enter field name: ")


def make_field_value_template() -> Optional[List[Union[int, str, float]]]:
    type = handle_type_input()
    if type in ["int", "float"]:
        if type == "int":
            min = handle_int_min_max_values("min")
            max = handle_int_min_max_values("max")
        if type == "float":
            min = handle_float_min_max_values("min")
            max = handle_float_min_max_values("max")
        return [type, min, max]
    elif type == "list":
        template = [type]
        list_template = make_field_value_template_for_lists()
        for value in list_template:
            template.append(value)
        return template
    else:
        return [type]


def make_field_value_template_for_lists():
    list_type = (
        input("Enter which type will be in the list(string, int, list): ")
        .strip()
        .lower()
    )
    if list_type in ["int", "float"]:
        if list_type == "int":
            min = handle_int_min_max_values("min")
            max = handle_int_min_max_values("max")
            list_lenght = int(input("How long the list will be?: ").strip())
            return [list_type, min, max, list_lenght]
        if list_type == "float":
            min = handle_float_min_max_values("min")
            max = handle_float_min_max_values("max")
            list_lenght = int(input("How long the list will be?: ").strip())
            return [list_type, min, max, list_lenght]
    else:
        list_lenght = int(input("How long the list will be?: ").strip())
        return [list_type, list_lenght]


def handle_type_input():
    while True:
        type = (
            input("Enter field value type(string, number(float, int), list, date): ")
            .strip()
            .lower()
        )
        if type not in ["int", "float", "string", "list","date"]:
            print("wrong type")
            continue
        else:
            break
    return type


def handle_float_min_max_values(min_or_max: str):
    while True:
        try:
            return float(input(f"Enter field {min_or_max} value(number): ").strip())
        except ValueError:
            print("wrong type")
            continue


def handle_int_min_max_values(min_or_max: str):
    while True:
        try:
            return int(input(f"Enter field {min_or_max} value(number): ").strip())
        except ValueError:
            print("wrong type")
            continue


def generate_value(type, min=None, max=None) -> Optional[Union[int, str, float]]:
    if type == "date":
        now = datetime.now()
        past_date = now - timedelta(days=1095)
        timestamp_now = now.replace(tzinfo=timezone.utc).timestamp()
        past_timestamp = past_date.replace(tzinfo=timezone.utc).timestamp()
        random_utc = random.uniform(past_timestamp, timestamp_now)
        return datetime.utcfromtimestamp(random_utc).strftime("%Y-%m-%d")
    if type == "string":
        r = RandomWords()
        return r.get_word()
    if type == "int":
        return random.randint(min, max)
    if type == "float":
        return round(random.uniform(min, max),2)


def get_number_of_docs_to_create() -> int:
    while True:
        try:
            return int(input("How mano documents to create?: "))
        except ValueError:
            print("Use integers!")
            continue
