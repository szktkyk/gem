import json
import pandas as pd
import re


def making_list_fig1(path, categori_str):
    f = open(path)
    json_list = json.load(f)
    species_list = []
    count_list = []
    for a_dict in json_list:
        if a_dict["category"] == categori_str:
            species_list.append(a_dict["organism"])
            count_list.append(a_dict["count"])
    return count_list, species_list


f = open("../json/20220827_ge_metadata.json")
json_list = json.load(f)

new_list = []
for a_dict in json_list:
    pubmed_id = a_dict["pubmed_id"]
    pubmed_url = a_dict["pubmed_uri"]
    pmid = "[{}]({})".format(pubmed_id, pubmed_url)
    # print(pmid)
    genesymbol = a_dict["genesymbol"]
    gene_url = a_dict["gene_url"]
    gene = "[{}]({})".format(genesymbol, gene_url)
    # rnaseq = a_dict["RNA-seq"]
    # geoid = re.findall(r">(.+)<", rnaseq)
    # print(geoid)
    # geourl = re.findall(r"\'.*\'", rnaseq)
    # geo = "[{}]({})".format(geoid[0], geourl[0])
    # biopro = a_dict["biopro_id"]
    # bpid = re.findall(r"\>.*\<", biopro)
    # bpurl = re.findall(r"\'.*\'", biopro)
    # bp = "[{}]({})".format(bpid[0], bpurl[0])

    metadata = {
        "getool": a_dict["getool"],
        "pmid": pmid,
        "pubtitle": a_dict["pubtitle"],
        "pubdate": a_dict["pubdate"],
        "organism_name": a_dict["organism_name"],
        "genesymbol": gene,
        "editing type": a_dict["editing type"],
        "gene_counts": a_dict["gene_counts"],
        # "bioproid": bp,
        # "RNA-seq": geo,
        "vector": a_dict["vector"],
        # "cellline": a_dict["cellline"],
        # "tissue": a_dict["tissue"],
        # "Mutation_type": a_dict["Mutation_type"],
    }
    new_list.append(metadata)


# exit()
with open(f"/Users/suzuki/gem/json/20220917_ge_metadata.json", "w") as f:
    json.dump(new_list, f, indent=3)

exit()

path = "../json/metastanza_fig2_20220827.json"
# cas9_count_list, species_list = making_list_fig1(path, "CRISPR-Cas9")
talen_count_list, talen_species_list = making_list_fig1(path, "TALEN")
zfn_count_list, zfn_species_list = making_list_fig1(path, "ZFN")
cas12_count_list, cas12_species_list = making_list_fig1(path, "CRISPR-Cas12")
cas3_count_list, cas3_species_list = making_list_fig1(path, "CRISPR-Cas3")
be_count_list, be_species_list = making_list_fig1(path, "Base editor")
pe_count_list, pe_species_list = making_list_fig1(path, "Prime editor")

# print(cas9_count_list)
print(talen_count_list)
print(talen_species_list)
print(zfn_count_list)
print(zfn_species_list)
print(cas12_count_list)
print(cas12_species_list)
print(cas3_count_list)
print(cas3_species_list)
print(be_count_list)
print(be_species_list)
print(pe_count_list)
print(pe_species_list)

exit()


path = "../json/metastanza_fig4_20220827.json"
cas9_count_list = making_list_fig1(path, "CRISPR-Cas9")
talen_count_list = making_list_fig1(path, "TALEN")
zfn_count_list = making_list_fig1(path, "ZFN")
cas12_count_list = making_list_fig1(path, "CRISPR-Cas12")
cas3_count_list = making_list_fig1(path, "CRISPR-Cas3")
be_count_list = making_list_fig1(path, "Base editor")
pe_count_list = making_list_fig1(path, "Prime editor")

print(cas9_count_list)
print(talen_count_list)
print(zfn_count_list)
print(cas12_count_list)
print(cas3_count_list)
print(be_count_list)
print(pe_count_list)
