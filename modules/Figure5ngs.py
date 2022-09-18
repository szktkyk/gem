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

biopro_cas9 = []
biopro_talen = []
biopro_zfn = []
biopro_cas12 = []
biopro_cas3 = []
biopro_be = []
biopro_pe = []
rnaseq_cas9 = []
rnaseq_talen = []
rnaseq_zfn = []
rnaseq_cas12 = []
rnaseq_cas3 = []
rnaseq_be = []
rnaseq_pe = []
for a_dict in json_list:
    if a_dict["biopro_id"] is not None:
        if a_dict["getool"] == "CRISPR-Cas9":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_cas9.append({a_dict["getool"]: bioproid})
        elif a_dict["getool"] == "TALEN":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_talen.append({a_dict["getool"]: bioproid})
        elif a_dict["getool"] == "ZFN":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_zfn.append({a_dict["getool"]: bioproid})
        elif a_dict["getool"] == "CRISPR-Cas12":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_cas12.append({a_dict["getool"]: bioproid})
        elif a_dict["getool"] == "CRISPR-Cas3":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_cas3.append({a_dict["getool"]: bioproid})
        elif a_dict["getool"] == "Base editor":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_be.append({a_dict["getool"]: bioproid})
        elif a_dict["getool"] == "Prime editor":
            bioproids = a_dict["biopro_id"].split(",")
            for bioproid in bioproids:
                biopro_pe.append({a_dict["getool"]: bioproid})

    if a_dict["RNA-seq"] is not None:
        if a_dict["getool"] == "CRISPR-Cas9":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_cas9.append({a_dict["getool"]: rnaseqid})
        elif a_dict["getool"] == "TALEN":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_talen.append({a_dict["getool"]: rnaseqid})
        elif a_dict["getool"] == "ZFN":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_zfn.append({a_dict["getool"]: rnaseqid})
        elif a_dict["getool"] == "CRISPR-Cas12":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_cas12.append({a_dict["getool"]: rnaseqid})
        elif a_dict["getool"] == "CRISPR-Cas3":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_cas3.append({a_dict["getool"]: rnaseqid})
        elif a_dict["getool"] == "Base editor":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_be.append({a_dict["getool"]: rnaseqid})
        elif a_dict["getool"] == "Prime editor":
            rnaseqids = a_dict["RNA-seq"].split(",")
            for rnaseqid in rnaseqids:
                rnaseq_pe.append({a_dict["getool"]: rnaseqid})


print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_cas9)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_talen)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_zfn)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_cas12)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_cas3)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_be)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in biopro_pe)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_cas9)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_talen)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_zfn)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_cas12)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_cas3)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_be)]))
print(len([dict(s) for s in set(frozenset(d.items()) for d in rnaseq_pe)]))
exit()

biopro_list = []
rnaseq_list = []
for a_dict in new_list:
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
