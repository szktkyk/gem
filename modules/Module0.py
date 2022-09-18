# from ast import IsNot
# from tkinter.tix import Tree
import requests
import xml.etree.ElementTree as ET
import json
import pandas as pd

# Essential Modules


def generate_chunked_id_list(id_list, max_len) -> list:
    """
    Parameters:
    ------
    id_list: list
        A list that will be splited

    max_len: int
        Number of elements in the list after splitting

    Returns:
    ------
    list_of_id_list: list
        A list contains splited lists
    """
    return [id_list[i : i + max_len] for i in range(0, len(id_list), max_len)]


def use_eutils(api_url):
    """
    function to use API

    Parameters:
    -----
    api_url: str
        URL for API

    Return:
    --------
    tree: xml
        Output in XML

    """
    req = requests.get(api_url)
    req.raise_for_status()
    tree = ET.fromstring(req.content)
    return tree


def ParseFromJson(path: str, key: str) -> list:
    """
    Parser to get the desired information from Json file.

    Parameters:
    -------
    path: str
        Path to Json file (including file name)
    key: str
        Dict key for the desired information

    Returns:
    -------
    list1: list
        A list of desired information
    """
    with open(path) as f:
        json_list = json.load(f)

    list1 = []

    for a_dict in json_list:
        info1 = a_dict[key]
        list1.append(info1)

    return list1


def join_two_jsons(path1: str, path2: str) -> list:
    """
    Joined two json file without redunduncy

    Parameters:
    -----------------
    path1: str
        path to json file1

    path2: str
        path to json file2

    Returns:
    ------------------
    json_list2: list
        A list contains joined json

    """
    f = open(path1)
    json_list1 = json.load(f)
    f2 = open(path2)
    json_list2 = json.load(f2)

    for a_dict in json_list1:
        if a_dict in json_list2:
            pass
        else:
            json_list2.append(a_dict)
            print(a_dict)
    return json_list2


def del_key_json(json_list: list, key: str) -> list:
    """
    Delete dict keys in json file

    Parameters:
    ---------------
    json_list: list
        A list that contains json

    key: str
        A dict key that will be deleted from json

    Returns:
    -----------------
    json_list: list
        A list that contains json the key was deleted

    """
    for a_dict in json_list:
        del a_dict[key]
    return json_list


# path = "20220805_ge_metadata.json"
# recreate_json(path)
