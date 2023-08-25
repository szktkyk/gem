import ast
import pandas as pd
import datetime
import config
import csv



def get_datalist_from_log(logfilepath):
    extracted_genes = []
    extracted_disease = []
    extracted_tissue = []
    with open(logfilepath) as f:
        for line in f:
            if line.startswith("{'pmid':"):
                line_dict = ast.literal_eval(line)
                extracted_genes.append(line_dict)
            if line.startswith("{'disease':"):
                line_dict = ast.literal_eval(line)
                extracted_disease.append(line_dict)
            if line.startswith("{'tissue':"):
                line_dict = ast.literal_eval(line)
                extracted_tissue.append(line_dict)
            else:
                continue


    return extracted_genes, extracted_disease, extracted_tissue


# print(len(pmids))
# print(pmids.index("33432361"))
# new_pmids = pmids[9474:]
# print(new_pmids)
# exit()

logfilepath1 = "./log/20230817_03_log2.txt"
extracted_genes, extracted_disease, extracted_tissue = get_datalist_from_log(logfilepath1)

field_name_gene = [
    "pmid",
    "species",
    "gene",
]
field_name_disease = [
    "pmid",
    "disease",
]
field_name_tissue = [
    "pmid",
    "tissue",
]
with open(
    f"./csv_gitignore/{config.date}_gene_annotations.csv",
    "w",
) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_name_gene)
    writer.writeheader()
    writer.writerows(extracted_genes)

with open(
    f"./csv_gitignore/{config.date}_disease_annotations.csv",
    "w",
) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_name_disease)
    writer.writeheader()
    writer.writerows(extracted_disease)

with open(
    f"./csv_gitignore/{config.date}_tissue_annotations.csv",
    "w",
) as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_name_tissue)
    writer.writeheader()
    writer.writerows(extracted_tissue)


