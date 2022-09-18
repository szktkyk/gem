import csv
import pandas as pd
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")
# date = "20220820"

path_tax = "../csv/tax_list.csv"
path_g2p = f"../data/{date}/{date}_g2p_updated.tsv"


def main():
    calculate_genecounts(path_g2p, path_tax)


def calculate_genefreq(path_gene2pubmed: str, path_tax: str) -> csv:
    """
    Parameters:
    -------------
    path_gene2pubmed: str
        path to gene2pubmed.csv

    path_tax: str
        path to the csv file containing pathid:name information

    Returns:
    --------------
    taxid_genesfreq.csv: csv
        A csv file for each taxonomy (geneid:genefreq)

    """
    df_gene2pubmed = pd.read_csv(path_gene2pubmed, sep="\t")
    df_tax = pd.read_csv(path_tax, sep=",")
    # 生物種ごとにgenefreqを計算する。
    for taxid in df_tax["taxid"]:
        df_taxid = df_gene2pubmed.loc[df_gene2pubmed["#tax_id"] == taxid]
        # print(df_taxid)
        geneids = df_taxid["GeneID"]
        genes_freq = geneids.value_counts(normalize=True)
        genes_freq.to_csv("../genesfreq/{}_genesfreq.csv".format(taxid))
    return None


def calculate_genecounts(path_gene2pubmed: str, path_tax: str) -> csv:
    """
    Parameters:
    -------------
    path_gene2pubmed: str
        path to gene2pubmed.csv

    path_tax: str
        path to the csv file containing pathid:name information

    Returns:
    --------------
    taxid_genecounts.csv: csv
        A csv file for each taxonomy (geneid:genecounts)

    """
    df_gene2pubmed = pd.read_csv(path_gene2pubmed, sep="\t")
    df_tax = pd.read_csv(path_tax, sep=",")
    # 生物種ごとにgenefreqを計算する。
    for taxid in df_tax["taxid"]:
        df_taxid = df_gene2pubmed.loc[df_gene2pubmed["#tax_id"] == taxid]
        # print(df_taxid)
        geneids = df_taxid["GeneID"]
        genes_counts = geneids.value_counts()
        genes_counts.to_csv("../genecounts/{}_genescounts.csv".format(taxid))
    return None


if __name__ == "__main__":
    main()
