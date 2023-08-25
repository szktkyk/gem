import re
import datetime
import requests
import xml.etree.ElementTree as ET


def get_text_by_tree(treepath, element):
    """
    Parameters:
    ------
    treepath: str
        path to the required information

    element: str
        tree element

    Returns:
    ------
    information: str
        parsed information from XML

    None: Null
        if information could not be parsed.

    """
    if element.find(treepath) is not None:
        return element.find(treepath).text
    else:
        return ""

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

# check candidate species from the specific section
def get_annotation_from_section(element, section:str):
    """
    Parameters:
    -------------
    element:XML
    section:str

    Returns:
    ----------------
    elements:list
        A list of elements of annotations in the specific section
    
    """
    species = []
    passages = element.findall("passage")
    for passage in passages:
        if passage.find("infon").text == section:
            annotations = passage.findall("annotation")
        else:
            annotations = None
            continue
    return annotations


# check candidate genes and diseases from title and abstract sections
def get_annotation_ptc(element):
    """
    Parameters:
    -------------
    element:XML

    Returns:
    ----------------
    species:list
        a list of annotation genes and diseases in title and abstract sections
    """
    genes = []
    disease = []
    for passage in element:
        ans = passage.findall("annotation")

        for a in ans:
            if a.find("infon[@key='type']").text == "Gene":
                try:
                    genes.append(a.find("infon[@key='identifier']").text)
                except:
                    continue

            if a.find("infon[@key='type']").text == "Disease":
                try:
                    disease.append(a.find("text").text)
                except:
                    continue

    return genes, disease


