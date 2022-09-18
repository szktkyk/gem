from ast import IsNot
from operator import is_not
from re import I
import pandas as pd
import matplotlib.pyplot as plt
import json
from Module0 import ParseFromJson
import collections

date = "20220827"

f = open(f"../json/{date}_ge_metadata.json")
json_list = json.load(f)

y_list = []
tax_list = []
for a_dict in json_list:
    if a_dict["organism_name"] is not None:
        tax_name = a_dict["organism_name"]
        # print(tax_name)
        tax_list.append(tax_name)
        y_list.append({tax_name: a_dict["getool"]})


# print(y_list)
# print(tax_list)
tax_list_order = []
count_species = collections.Counter(tax_list).most_common()
for count_specie in count_species:
    tax_list_order.append(count_specie[0])

print(f"tax_list_order{tax_list_order}")

# exit()

barchart_list = []
# tax_list = ParseFromJson("./json/20220718_ge_metadata_working.json", "organism_name")
# tax_list = list(set(tax_list))
# print(tax_list)

# df_order = pd.read_csv("./csv/organism_order.csv", sep=",")

# print(tax_list)
for organism_order in range(0, 31):
    organism_name = tax_list_order[organism_order]
    # order_row = df_order[df_order["organism"] == organism_name]
    # print(order_row)
    # organism_order = int(order_row["number"].values[0])
    # print(organism_name)

    crispr_cas9 = y_list.count({organism_name: "CRISPR-Cas9"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas9",
            "category_order": 0,
            "organism": organism_name,
            "organism_order": organism_order,
            "count": crispr_cas9,
        }
    )

    talen = y_list.count({organism_name: "TALEN"})
    barchart_list.append(
        {
            "category": "TALEN",
            "category_order": 1,
            "organism": organism_name,
            "organism_order": organism_order,
            "count": talen,
        }
    )
    zfn = y_list.count({organism_name: "ZFN"})
    barchart_list.append(
        {
            "category": "ZFN",
            "category_order": 2,
            "organism": organism_name,
            "organism_order": organism_order,
            "count": zfn,
        }
    )
    cas12 = y_list.count({organism_name: "CRISPR-Cas12"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas12",
            "category_order": 3,
            "organism": organism_name,
            "organism_order": organism_order,
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
    cas3 = y_list.count({organism_name: "CRISPR-Cas3"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas3",
            "category_order": 4,
            "organism": organism_name,
            "organism_order": organism_order,
            "count": cas3,
        }
    )
    be = y_list.count({organism_name: "Base editor"})
    barchart_list.append(
        {
            "category": "Base editor",
            "category_order": 5,
            "organism": organism_name,
            "organism_order": organism_order,
            "count": be,
        }
    )
    pe = y_list.count({organism_name: "Prime editor"})
    barchart_list.append(
        {
            "category": "Prime editor",
            "category_order": 6,
            "organism": organism_name,
            "organism_order": organism_order,
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
    # sacas9 = y_list.count({organism_name: "SaCas9"})
    # barchart_list.append(
    #     {
    #         "category": "SaCas9",
    #         "category_order": 9,
    #         "organism": organism_name,
    #         "organism_order": organism_order,
    #         "count": sacas9,
    #     }
    # )

barchart_list2 = sorted(barchart_list, key=lambda x: x["organism_order"])
print(barchart_list2)


with open(f"../json/metastanza_fig2_{date}.json", "w") as f:
    json.dump(barchart_list2, f, indent=3)
