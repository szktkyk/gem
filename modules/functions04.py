import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from requests.exceptions import HTTPError
import re
import pandas as pd

def parse_bioproid(texts: str) -> list:
    """
    Parameters:
    -------------------
    texts:str
        texts to parse editing types

    Returns:
    ---------------
    bioproid: list or Null
        if bioproid is found, returned as list
    """
    biopro_pattern = re.compile("PRJ.A[0-9]{5,6}|PRJ.A.[0-9]{5,6}")
    if re.search(biopro_pattern, texts):
        bioproid = re.findall(biopro_pattern, texts)
        bioproid = list(set(bioproid))
    else:
        bioproid = []
    return bioproid


def parse_addgene(texts: str, path: str) -> str or None:
    """
    Parameters:
    -------------
    texts:str
        texts to parse editing types

    path: str
        path to addgene.csv

    Returns:
    --------------
    vector_namelist: list
        addgeneID is extracted from Methods, and if it matches the dictionary, the vector name is put in the list.


    """
    df_csv = pd.read_csv(path, sep=",")
    addgeneid_pattern = re.compile("[0-9]{5,10}")
    addgeneids = re.findall(addgeneid_pattern, texts)
    addgeneids = list(set(addgeneids))
    vector_namelist = []
    for addgeneid in addgeneids:
        try:
            row = df_csv[df_csv["addgeneid"] == int(addgeneid)]
            vector_namelist.append(row["vectorname"].values[0])
        except:
            continue
    if vector_namelist != []:
        vectors = ",".join(vector_namelist)
    else:
        vectors = None
    return vectors


def parse_geo(texts: str) -> list:
    """
    Parameters:
    -------------------
    texts:str
        texts (METHODS etc) to parse NCBI GEO ID

    Returns:
    ---------------
    geoid: list or Null
        if geoid is found, returned as list

    """
    geo_pattern = re.compile("GSE[0-9]{5,6}|GSE.[0-9]{5,6}")
    if re.search(geo_pattern, texts):
        geoid = re.findall(geo_pattern, texts)
        geoid = list(set(geoid))
    else:
        geoid = []
    return geoid

def get_xml_from_pmcid(pmcid_str):
    """
    Get full text XML file from pmcid. only one ID at a time is possible.

    Parameters:
    ------
    pmcid_str: str
        a pmcid

    Returns:
    -------
    tree: tree
        tree element in XML
    """
    fulltext_api_url = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/{}/unicode"
    api_url = fulltext_api_url.format(pmcid_str)
    print(api_url)
    req = requests.get(api_url)
    tree = ET.fromstring(req.content)
    # tree_text = minidom.parseString(ET.tostring(tree)).toprettyxml(indent="    ")
    return tree

def parse_section_pmc(tree: str, section: str) -> list:
    """
    Parameters:
    -----------
    tree: str
        PMC fulltext tree element in XML

    section: str
        name of the pmc section (RESULTS, METHODS, etc) to parse

    Returns:
    -------------
    methods_fulltext: list
        A list of all strings from the chosen section
    """

    section_fulltext_list = []
    passages = tree.findall("./document/passage")
    for passage in passages:
        if passage.find("infon").text == section:
            part_of_section = passage.find("text").text
            section_fulltext_list.append(part_of_section)

    return section_fulltext_list