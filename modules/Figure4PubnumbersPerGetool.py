import json
from Module0 import *
from frozendict import frozendict


# t_delta = datetime.timedelta(hours=9)
# JST = datetime.timezone(t_delta, "JST")
# now = datetime.datetime.now(JST)
# date = now.strftime("%Y%m%d")
date = "20220827"

f = open(f"../json/{date}_ge_metadata.json")
json_list = json.load(f)

y_list = []
for a_dict in json_list:
    # pubyear = a_dict["pubdate"].split("-")[0]
    # print(pubyear)
    # pmid = a_dict["pubmed_id"]
    y_list.append(
        {
            "pubyear": a_dict["pubdate"].split("-")[0],
            "getool": a_dict["getool"],
            "pmid": a_dict["pubmed_id"],
        }
    )
print(len(y_list))

new_list = [dict(s) for s in set(frozenset(d.items()) for d in y_list)]
# print(new_list)

y_new_list = []
for dict in new_list:
    y_new_list.append({dict["pubyear"]: dict["getool"]})

barchart_list = []
for year in range(2010, 2023):
    crispr_cas9 = y_new_list.count({str(year): "CRISPR-Cas9"})
    pubyear_order = year - 2010
    barchart_list.append(
        {
            "category": "CRISPR-Cas9",
            "category_order": 0,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": crispr_cas9,
        }
    )
    talen = y_new_list.count({str(year): "TALEN"})
    barchart_list.append(
        {
            "category": "TALEN",
            "category_order": 1,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": talen,
        }
    )
    zfn = y_new_list.count({str(year): "ZFN"})
    barchart_list.append(
        {
            "category": "ZFN",
            "category_order": 2,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": zfn,
        }
    )
    cas12 = y_new_list.count({str(year): "CRISPR-Cas12"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas12",
            "category_order": 3,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": cas12,
        }
    )
    # cas13 = y_list.count({str(year): "CRISPR-Cas13"})
    # barchart_list.append(
    #     {
    #         "category": "CRISPR-Cas13",
    #         "category_order": 4,
    #         "pubyear": str(year),
    #         "pubyear_order": pubyear_order,
    #         "count": cas13,
    #     }
    # )
    cas3 = y_new_list.count({str(year): "CRISPR-Cas3"})
    barchart_list.append(
        {
            "category": "CRISPR-Cas3",
            "category_order": 4,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": cas3,
        }
    )
    be = y_new_list.count({str(year): "Base editor"})
    barchart_list.append(
        {
            "category": "Base editor",
            "category_order": 5,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": be,
        }
    )
    pe = y_new_list.count({str(year): "Prime editor"})
    barchart_list.append(
        {
            "category": "Prime editor",
            "category_order": 6,
            "pubyear": str(year),
            "pubyear_order": pubyear_order,
            "count": pe,
        }
    )
    # pitch = y_list.count({str(year): "PITCh"})
    # barchart_list.append(
    #     {
    #         "category": "PITCh",
    #         "category_order": 8,
    #         "pubyear": str(year),
    #         "pubyear_order": pubyear_order,
    #         "count": pitch,
    #     }
    # )
    # sacas9 = y_list.count({str(year): "SaCas9"})
    # barchart_list.append(
    #     {
    #         "category": "SaCas9",
    #         "category_order": 9,
    #         "pubyear": str(year),
    #         "pubyear_order": pubyear_order,
    #         "count": sacas9,
    #     }
    # )

print(barchart_list)

with open(f"../json/metastanza_fig4_{date}.json", "w") as f:
    json.dump(barchart_list, f, indent=3)
