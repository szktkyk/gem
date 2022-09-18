import pandas as pd
import json
from Module0 import *
import collections

date = "20220827"

f = open(f"../json/{date}_ge_metadata.json")
json_list = json.load(f)

all_gene_list = []
getool_gene_list = []
for a_dict in json_list:
    genesymbol = a_dict["genesymbol"]
    getool = a_dict["getool"]
    organism_name = a_dict["organism_name"]
    if genesymbol is not None:
        all_gene_list.append("{} ({})".format(genesymbol, organism_name))
        getool_gene_list.append({"{} ({})".format(genesymbol, organism_name): getool})

gene_list_order = []
count_genes = collections.Counter(all_gene_list).most_common()
print(count_genes)
for count_gene in count_genes:
    gene_list_order.append(count_gene[0])


barchart_list = []
# tax_list = ParseFromJson("./json/20220718_ge_metadata_working.json", "organism_name")
# tax_list = list(set(tax_list))
# print(tax_list)

# df_order = pd.read_csv("./csv/organism_order.csv", sep=",")

# print(tax_list)
for gene_order in range(0, 30):
    gene_name = gene_list_order[gene_order]
    # order_row = df_order[df_order["organism"] == organism_name]
    # print(order_row)
    # organism_order = int(order_row["number"].values[0])
    # print(organism_order)

    crispr_cas9 = getool_gene_list.count({gene_name: "CRISPR-Cas9"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas9",
            "category_order": 0,
            "gene": gene_name,
            "gene_order": gene_order,
            "count": crispr_cas9,
        }
    )
    talen = getool_gene_list.count({gene_name: "TALEN"})
    barchart_list.append(
        {
            "category": "TALEN",
            "category_order": 1,
            "gene": gene_name,
            "gene_order": gene_order,
            "count": talen,
        }
    )
    zfn = getool_gene_list.count({gene_name: "ZFN"})
    barchart_list.append(
        {
            "category": "ZFN",
            "category_order": 2,
            "gene": gene_name,
            "gene_order": gene_order,
            "count": zfn,
        }
    )
    cas12 = getool_gene_list.count({organism_name: "CRISPR-Cas12"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas12",
            "category_order": 3,
            "gene": organism_name,
            "gene_order": gene_order,
            "count": cas12,
        }
    )
    # cas13 = y_list.count({organism_name: "CRISPR-Cas13"})
    # barchart_list.append(
    #     {
    #         "category": "CRISPR-Cas13",
    #         "category_order": 4,
    #         "organism": organism_name,
    #         "organism_order": organism_order,
    #         "count": cas13,
    #     }
    # )
    cas3 = getool_gene_list.count({organism_name: "CRISPR-Cas3"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas3",
            "category_order": 4,
            "gene": organism_name,
            "gene_order": gene_order,
            "count": cas3,
        }
    )
    be = getool_gene_list.count({gene_name: "Base editor"})
    barchart_list.append(
        {
            "category": "Base editor",
            "category_order": 5,
            "gene": gene_name,
            "gene_order": gene_order,
            "count": be,
        }
    )
    pe = getool_gene_list.count({gene_name: "Prime editor"})
    barchart_list.append(
        {
            "category": "Prime editor",
            "category_order": 6,
            "gene": gene_name,
            "gene_order": gene_order,
            "count": pe,
        }
    )
    # pitch = y_list.count({organism_name: "PITCh"})
    # barchart_list.append(
    #     {
    #         "category": "PITCh",
    #         "category_order": 8,
    #         "organism": organism_name,
    #         "organism_order": organism_order,
    #         "count": pitch,
    #     }
    # )
    # sacas9 = getool_gene_list.count({gene_name: "SaCas9"})
    # barchart_list.append(
    #     {
    #         "category": "SaCas9",
    #         "category_order": 5,
    #         "gene": gene_name,
    #         "gene_order": gene_order,
    #         "count": sacas9,
    #     }
    # )
print(barchart_list)
barchart_list2 = sorted(barchart_list, key=lambda x: x["gene_order"])
# print(barchart_list2)


with open(f"../json/metastanza_fig3_{date}.json", "w") as f:
    json.dump(barchart_list2, f, indent=3)
