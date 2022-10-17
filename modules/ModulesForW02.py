import pandas as pd
from Module0 import *
from ftplib import FTP


def download_gene2pubmed():
    url = "ftp.ncbi.nlm.nih.gov"
    path = "/gene/DATA"
    ftp = FTP(url)
    ftp.login()
    ftp.cwd(path)
    with open("../csv_gitignore/gene2pubmed.gz", "wb") as f:
        ftp.retrbinary("RETR gene2pubmed.gz", f.write)
    ftp.quit()


def download_gene_info():
    url = "ftp.ncbi.nlm.nih.gov"
    path = "/gene/DATA"
    ftp = FTP(url)
    ftp.login()
    ftp.cwd(path)
    with open("../csv/gene_info.gz", "wb") as f:
        ftp.retrbinary("RETR gene_info.gz", f.write)
    ftp.quit()


# Matching with csv or tsv file
def match_with_csv(words: list, path: str, keyword1: str, keyword2: str) -> list:
    """
    Parameters:
    --------------
    words: list
        A list of words

    path: str
        path to csv file

    keyword1: str
        column name that contains information to be matched with words

    keyword2: str
        column name that contains information to be extracted

    Returns:
    ----------------
    matched_list: list
        a list of matched words
    """
    # Change the delimiter as appropriate
    # output as a list because there may be more than one matched words
    matched_list = []
    df_csv = pd.read_csv(path, sep=",")

    for word in words:
        # print(word)
        try:
            row = df_csv[df_csv[keyword1] == word]
            # print(row[keyword1].values[0])
            matched_list.append(row[keyword2].values[0])
        except:
            continue
    return matched_list


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


def match_with_tsv_capitalize(
    words: list, path: str, keyword1: str, keyword2: str
) -> list:
    """
    Same as `match_with_tsv` but word is capitalized
    """
    # 区切り文字は適宜変更する。
    df_csv = pd.read_csv(path, sep="\t")

    matched_list = []
    for word in words:
        # print(word)
        word = word.capitalize()
        # print(word)
        try:
            row = df_csv[df_csv[keyword1] == word]
            # print(row[keyword1].values[0])
            matched_list.append(row[keyword2].values[0])
        except:
            continue
    return matched_list


def match_with_tsv_upper(words: list, path: str, keyword1: str, keyword2: str) -> list:
    """
    Same as `match_with_tsv` but word is in uppercase
    """
    # 区切り文字は適宜変更する。
    df_csv = pd.read_csv(path, sep="\t")

    matched_list = []
    for word in words:
        # print(word)
        word = word.upper()
        try:
            row = df_csv[df_csv[keyword1] == word]
            # print(row[keyword1].values[0])
            matched_list.append(row[keyword2].values[0])
        except:
            continue
    return matched_list


def match_with_tsv_lower(words: list, path: str, keyword1: str, keyword2: str) -> list:
    """
    Same as `match_with_tsv` but word is in lowercase
    """
    # 区切り文字は適宜変更する。
    df_csv = pd.read_csv(path, sep="\t")

    matched_list = []
    for word in words:
        # print(word)
        word = word.lower()
        try:
            row = df_csv[df_csv[keyword1] == word]
            # print(row[keyword1].values[0])
            matched_list.append(row[keyword2].values[0])
        except:
            continue
    return matched_list


# using PubTator Central or PubTator
def get_annotations_ptc(tree):
    """
    Parameters:
    ---------------
    tree:xml

    Returns:
    ----------------
    genes:list
        a list of genesymbols obtained from PubTator Central

    species:list
        a list of species obtained from PubTator Central

    """
    genes = []
    species = []
    elements = tree.findall("./document/passage")
    for element in elements:
        if element.find("infon").text == "METHODS" or "ABSTRACT":
            ans = element.findall("annotation")
            for a in ans:
                if a.find("infon[@key='type']").text == "Species":
                    species.append(a.find("text").text)

        if element.find("infon").text == "RESULTS" or "ABSTRACT":
            ans = element.findall("annotation")
            for a in ans:
                if a.find("infon[@key='type']").text == "Gene":
                    genes.append(a.find("text").text)

    return genes, species


def pubtator_species_from_pmid(element):
    """
    Parameters:
    -------------
    element:XML

    Returns:
    ----------------
    species:list
        a list of annotation species in pubtator
    """
    species = []
    passages = element.findall("./passage/annotation")
    for passage in passages:
        if passage.find("infon[@key='type']").text == "Species":
            species.append(passage.find("text").text)
    return species


def pubtator_genes_from_pmid(element):
    """
    Parameters:
    -------------
    element:XML

    Returns:
    ----------------
    genes:list
        a list of annotation genes in pubtator
    """
    genes = []
    passages = element.findall("./passage/annotation")
    for passage in passages:
        if passage.find("infon[@key='type']").text == "Gene":
            genes.append(passage.find("text").text)
    return genes
