import pandas as pd
import json
import requests
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import csv
import datetime
import os
from dotenv import load_dotenv
from Module0 import *

load_dotenv()
# t_delta = datetime.timedelta(hours=9)
# JST = datetime.timezone(t_delta, "JST")
# now = datetime.datetime.now(JST)
# date = now.strftime("%Y%m%d")

# pmc_term = '"genome editing" OR "gene editing" OR CRISPR-Cas* OR cas9 OR cas12 OR cas3 OR sacas9 OR "CRISPR technology" OR "Transcription Activator-Like Effector Nucleases" OR "TAL effector" OR "TALEN" OR "guide RNA" OR sgRNA OR "Zinc finger nuclease" OR ZFN OR "Prime Editing" OR "Base editing" NOT ("Review"[Publication Type]) AND "pubmed pmc"[sb]'
pubmed_term = '"genome editing" OR "gene editing" OR CRISPR-Cas* OR cas9 OR cas12 OR cas3 OR sacas9 OR "CRISPR technology" OR "Transcription Activator-Like Effector Nucleases" OR "TAL effector" OR "TALEN" OR "guide RNA" OR sgRNA OR "Zinc finger nuclease" OR ZFN OR "Prime Editing" OR "Base editing" NOT ("Review"[Publication Type])'
# test_term = '"genome editing" AND "gene editing" AND "CRISPR Cas" AND cas9 AND cas12 AND cas3 OR sacas9 OR "CRISPR technology" OR "Transcription Activator-Like Effector Nucleases" OR "TAL effector" OR "TALEN" OR "guide RNA" OR "Zinc finger nuclease" AND "Prime Editing" OR "Base editing" NOT ("Review"[Publication Type])'


path = "/Users/suzuki/gem/mtrees2022.bin"
mtree = pd.read_csv(path, sep=";")
print(mtree.head)


def main():
    """
    use e-utilities to get publication details and to make a csv file
    """
    pmids_list = get_pmids(pubmed_term)
    print(f"number of pmids: {len(pmids_list)}")
    mesh_list = get_pubdetails(pmids_list, 200)
    print(mesh_list)
    print(len(mesh_list))


def get_pmids(term: str) -> list:
    """
    Make a list of pmids searched by specific term

    Prameters:
    ---------------
    term: str
        search term using for pubmed

    Returns:
    ----------------
    pmids_list: list
        A list of all the pmids resulted from the search term
    """
    api_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&datetype=edat&retmax=40000"
    tree = use_eutils(api_url.format(term))

    pmids_list = []

    for id in tree.findall("./IdList/Id"):
        pmid = id.text
        pmids_list.append(pmid)
    return pmids_list


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


def get_pubdetails(pmids: list, max_len: int) -> list:
    """
    Parameters:
    --------
    pmids: list
        a list of pmids

    max_len: int
        Number of elements in the list after splitting

    Returns:
    -------
    pmids_metadata:list
        a list containing dicts of publication details

    """

    list_of_chunked_pmids = generate_chunked_id_list(pmids, max_len)
    # pmids_metadata = []
    url_base = "https://eutils.ncbi.nlm.nih.gov/"

    mesh_list = []
    for a_chunked_pmids in list_of_chunked_pmids:
        # print(a_chunked_pmids)
        pmid_str = ",".join(a_chunked_pmids)
        epost_params = "entrez/eutils/epost.fcgi?db=pubmed&id={}&api_key={}"
        api1 = url_base + epost_params.format(pmid_str, os.getenv("api_key"))
        print(api1)
        print("connected to epost...")

        tree1 = use_eutils(api1)
        webenv = ""
        webenv = tree1.find("WebEnv").text
        esummary_params = "entrez/eutils/efetch.fcgi?db=pubmed&WebEnv={}&query_key=1&api_key={}&retmode=xml"
        api2 = url_base + esummary_params.format(webenv, os.getenv("api_key"))
        print("connected to efetch...")
        print(api2)
        tree2 = use_eutils(api2)

        for element in tree2.iter("PubmedArticle"):

            mesh_elements = element.findall(
                "./MedlineCitation/MeshHeadingList/MeshHeading"
            )
            for mesh in mesh_elements:
                element = mesh.find("DescriptorName")
                # print(element.text)
                # print(element.attrib)
            try:
                row = mtree[mtree["mesh"] == element.text]
                treeid = row["treeid"].values[0]
                # print(treeid)
                if treeid.startswith("B"):
                    mesh_list.append(element.text)
            except:
                continue

        mesh_list = list(set(mesh_list))
        print(mesh_list)

    return mesh_list


if __name__ == "__main__":
    main()
