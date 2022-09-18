import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from requests.exceptions import HTTPError
import re
import pandas as pd
from Module0 import *


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


def parse_editingtype(texts: str) -> list:
    """
    Parameter:
    ---------------
    tects:str
        texts to parse editing types

    Returns:
    ---------------
    editing_type: list
        determine the EDITING TYPE based on regular expression and make a list

    """
    knockout_pattern = re.compile(
        "KO.cell|knockout|knock.out|knocked.out|null.mutant|-/-|−/−", re.IGNORECASE
    )
    # ゲノム編集だと-/-この表記はあまり使わない??元からのKnockout系統の可能性もあり？生物種によって文化が違う

    knockin_pattern = re.compile("knock.in|knockin", re.IGNORECASE)

    editing_type = []
    # Knockdownはまた今度にする
    # knockdown_patterns = re.compile("knockdown", re.IGNORECASE)
    if re.search(knockout_pattern, texts):
        print(re.search(knockout_pattern, texts))
        editing_type.append("Knock-Out")

    if re.search(knockin_pattern, texts):
        print(re.search(knockin_pattern, texts))
        editing_type.append("Knock-in")

    editing_type = list(set(editing_type))
    return editing_type


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
        texts (METHODS etc) to parse editing types

    Returns:
    ---------------
    geoid: list or Null
        if geoid is found, returned as list

    """
    geo_pattern = re.compile("GSE[0-9]{5,6}|GSE.[0-9]{5,6}")
    rna_seq_pattern = re.compile("RNA-seq", re.IGNORECASE)
    if re.search(geo_pattern, texts) and re.search(rna_seq_pattern, texts):
        geoid = re.findall(geo_pattern, texts)
        geoid = list(set(geoid))
    else:
        geoid = []
    return geoid


def convert_geneid_to_genesymbol_str(geneid):
    """
    Parameters:
    --------------
    geneid: str

    Returns:
    --------------
    genesymbol: str

    """
    api_base = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id={}"
    )
    tree = use_eutils(api_base.format(geneid))
    genesymbol = tree.find("./DocumentSummarySet/DocumentSummary/Name").text
    return genesymbol


def match_with_tsv(words: list, path: str, keyword1: str, keyword2: str) -> list:
    """
    Same as `match_with_csv` but delimiter is "\t"
    """
    df_csv = pd.read_csv(path, sep="\t")

    matched_list = []
    for word in words:
        # print(word)
        try:
            row = df_csv[df_csv[keyword1] == word]
            # print(row[keyword1].values[0])
            matched_list.append(row[keyword2].values[0])
        except:
            continue
    return matched_list
