import pandas as pd
from modules.ModulesForW02 import *
import numpy as np
import time
import subprocess

# Download gene_info from ftp site to the local data directory (every 2 months?)
download_gene_info()
# gunzip gene_info
source_file = "../data/gene2pubmed.gz"
command = ["gunzip", source_file]
time.sleep(1)
subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print("gene_info is downloaded in the local data directory")

time.sleep(1)
command_format = "cat gene_info | awk '{ print $1, $2, $3}' > ../data/geneinfo.csv"
subprocess.call(command_format.split())

df_geneinfo = pd.read_csv("../data/geneinfo.csv", sep=" ")

df_dict = {}
for name, group in df_geneinfo.groupby("#tax_id"):
    df_dict[name] = group
    df_dict[name].to_csv(f"./gene_ref_test/{name}_genes.csv", sep="\t")

time.sleep(1)
command_remove1 = "rm ../data/gene_info"
command_remove2 = "rm ../data/geneinfo.csv"
subprocess.call(command_remove1.split())
time.sleep(1)
subprocess.call(command_remove2.split())
