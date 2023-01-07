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
import subprocess

load_dotenv()

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")
date = "20230107"

# pmc_term = '"genome editing" OR "gene editing" OR CRISPR-Cas* OR cas9 OR cas12 OR cas3 OR sacas9 OR "CRISPR technology" OR "Transcription Activator-Like Effector Nucleases" OR "TAL effector" OR "TALEN" OR "guide RNA" OR sgRNA OR "Zinc finger nuclease" OR ZFN OR "Prime Editing" OR "Base editing" NOT ("Review"[Publication Type]) AND "pubmed pmc"[sb]'
# pubmed_term = '"genome editing" OR "genome writing" OR "gene editing" OR CRISPR-Cas* OR cas9 OR cas12 OR cas3 OR sacas9 OR "CRISPR technology" OR "Transcription Activator-Like Effector Nucleases" OR "TAL effector" OR "TALEN" OR "guide RNA" OR sgRNA OR "Zinc finger nuclease" OR ZFN OR "Prime Editing" OR "Base editing" NOT ("Review"[Publication Type])'
# test_term = '"genome editing" mouse'
pubmed_term = 'CRISPR-tech* OR gene-edit* OR genome-edit* OR genome-writ* OR CRISPR-Cas* OR "CRISPR-Associated Proteins"[MeSH] OR "CRISPR-Associated Protein 9"[MeSH] OR cas9 OR cas12 OR cas3 OR sacas9 OR "Transcription Activator-Like Effector Nucleases" OR TAL-effector* OR TALEN OR guide-RNA* OR sgRNA OR zinc-finger-nuclease* OR ZFN OR "Prime editing" OR prime-edit* OR "Base editing" OR base-edit* NOT ("Review"[Publication Type])'

# esearch -db pubmed -query 'query'| efetch -format uid > date_efetch.txt

def main():
    """
    use e-utilities to get publication details and to make a csv file
    """
    pmids_list = get_pmids_new(f"/Users/suzuki/{date}_efetch_diff.txt")
    print(f"number of pmids: {len(pmids_list)}")
    pmids_metadata = get_pubdetails(pmids_list, 150)
    field_name = [
        "pmid",
        "doi",
        "pmcid",
        "title",
        "pubdate",
        "substances",
        "keywordlist",
        "abstract",
        "mesh",
    ]

    # Make a directory if not exist
    new_dir_path = f"../data/{date}"
    if not os.path.isdir(new_dir_path):
        os.mkdir(new_dir_path)

    with open(
        f"../data/{date}/{date}_pubdetails_edirect.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(pmids_metadata)


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


def get_pmids_new(file_path: str) -> list:
    """
    Make a list of pmids searched by specific term

    Prameters:
    ---------------
    term: file_path
        A txt file containing all the necessary pmids

    Returns:
    ----------------
    pmids_list: list
        A list of all the pmids resulted from the search term
    """
    with open(file_path) as f:
        lines = f.readlines()
    
    pmids_list = [line.rstrip('\n') for line in lines]

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
    pmids_metadata = []

    for a_chunked_pmids in list_of_chunked_pmids:
        # print(a_chunked_pmids)
        pmid_str = ",".join(a_chunked_pmids)
        # epost_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pubmed&id={}&api_key={}"
        # api1 = epost_params.format(pmid_str, os.getenv("api_key"))
        # print(api1)
        # print("connected to epost...")

        # tree1 = use_eutils(api1)
        # webenv = ""
        # webenv = tree1.find("WebEnv").text
        # esummary_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&WebEnv={}&query_key=1&api_key={}&retmode=xml"
        # api2 = esummary_params.format(webenv, os.getenv("api_key"))
        # print("connected to efetch...")
        # print(api2)
        req = subprocess.run(["efetch","-db","pubmed","-id","{}".format(pmid_str),"-format","xml"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        req2 = req.stdout.decode("utf8")
        # print(type(req.stdout.decode("utf8")))
        # exit()
        try:
            tree2 = ET.fromstring(req2)
        except:
            print("error at {}".format(pmid_str))
            continue

        for element in tree2.iter("PubmedArticle"):

            pmid = get_text_by_tree("./MedlineCitation/PMID", element)
            doiid = get_text_by_tree(
                "./PubmedData/ArticleIdList/ArticleId[@IdType='doi']",
                element,
            )
            pmcid = get_text_by_tree(
                "./PubmedData/ArticleIdList/ArticleId[@IdType='pmc']",
                element,
            )
            if pmcid == "":
                pmcid = "Not found"

            element_title = element.find("./MedlineCitation/Article/ArticleTitle")
            title = "".join(element_title.itertext())
            try:
                pubdate_year = element.find(
                    "./MedlineCitation/Article/ArticleDate/Year"
                ).text
                pubdate_month = element.find(
                    "./MedlineCitation/Article/ArticleDate/Month"
                ).text
                pubdate_day = element.find(
                    "./MedlineCitation/Article/ArticleDate/Day"
                ).text
            except:
                pubdate_year = element.find(
                    "./PubmedData/History/PubMedPubDate/Year"
                ).text
                pubdate_month = element.find(
                    "./PubmedData/History/PubMedPubDate/Month"
                ).text
                pubdate_day = element.find(
                    "./PubmedData/History/PubMedPubDate/Day"
                ).text

            pubdate = "{}-{}-{}".format(pubdate_year, pubdate_month, pubdate_day)

            substances_list = []
            substances = element.findall(
                "MedlineCitation/ChemicalList/Chemical/NameOfSubstance"
            )
            for substance in substances:
                substances_list.append(substance.text)

            keywords = []
            keywordlist = element.findall("MedlineCitation/KeywordList/Keyword")
            for keyword in keywordlist:
                keywords.append(keyword.text)

            element_abstract = element.find(
                "./MedlineCitation/Article/Abstract/AbstractText"
            )
            try:
                abstract = "".join(element_abstract.itertext())
            except:
                abstract = ""

            mesh_list = []
            mesh_elements = element.findall(
                "./MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"
            )
            for mesh in mesh_elements:
                mesh_list.append(mesh.text)

            pmids_metadata.append(
                {
                    "pmid": pmid,
                    "doi": doiid,
                    "pmcid": pmcid,
                    "title": title,
                    "pubdate": pubdate,
                    "substances": substances_list,
                    "keywordlist": keywords,
                    "abstract": abstract,
                    "mesh": mesh_list,
                }
            )


    return pmids_metadata


if __name__ == "__main__":
    main()
