import pandas as pd
import re
from ModulesForW02 import *
import collections
import ast
import datetime
import subprocess
import time

"""
MeSH→PubTatorCentral
"""


path = "/Users/suzuki/gem/csv/mtrees2022.bin"
mtree = pd.read_csv(path, sep=";")
# print(mtree.head)

# 37 species
tax_patterns = {
    "Anopheles gambiae": re.compile(
        "A. gambiae|An. gambiae|Anopheles gambiae|Anopheles", re.IGNORECASE
    ),
    "Apis mellifera": re.compile("Apis.mellifera|honeybee", re.IGNORECASE),
    "Arabidopsis thaliana": re.compile("Arabidopsis|Col-0|A. thaliana", re.IGNORECASE),
    "Arachis hypogaea": re.compile("peanut", re.IGNORECASE),
    "Bombyx mori": re.compile("silkworm|Bombyx.mori", re.IGNORECASE),
    "Bos taurus": re.compile("bovine", re.IGNORECASE),
    "Brassica napus": re.compile("B. napus|Brassica.napus", re.IGNORECASE),
    "Brassica rapa": re.compile(
        "Brassica.rapa|B. rapa|chinese.cabbage|turnip", re.IGNORECASE
    ),
    "Caenorhabditis elegans": re.compile(
        "C.{1,2}elegans",
        re.IGNORECASE,
    ),
    "Callithrix jacchus": re.compile("Callithrix.jacchus|marmoset", re.IGNORECASE),
    "Canis lupus familiaris": re.compile("dog", re.IGNORECASE),
    "Capra hircus": re.compile("goat|capra.hircus", re.IGNORECASE),
    "Citrus sinensis": re.compile("orange|grapefruit", re.IGNORECASE),
    "Cucumis melo": re.compile("Cucumis.melo", re.IGNORECASE),
    "Danio rerio": re.compile("zebrafish|Danio.rerio", re.IGNORECASE),
    "Drosophila melanogaster": re.compile("Drosophila|D. melanogaster", re.IGNORECASE),
    "Felis catus": re.compile("Felis.catus|cats", re.IGNORECASE),
    "Gallus gallus": re.compile("Gallus.gallus|chicken", re.IGNORECASE),
    "Glycine max": re.compile("Glycine.max|soya.bean|soybean", re.IGNORECASE),
    "Gossypium hirsutum": re.compile(
        "Gossypium.hirsutum|upland.cotton|mexican.cotton", re.IGNORECASE
    ),
    "Homo sapiens": re.compile("human|homo.sapiens", re.IGNORECASE),
    "Hordeum vulgare": re.compile("barley", re.IGNORECASE),
    # Ictalurusの遺伝子探索について、小文字にするか悩み中。
    "Ictalurus punctatus": re.compile("Ictalurus.punctatus|catfish", re.IGNORECASE),
    "Lentinula edodes": re.compile("mushroom", re.IGNORECASE),
    "Manihot esculenta": re.compile("cassava", re.IGNORECASE),
    "Mesocricetus auratus": re.compile("BHK.21|hamster", re.IGNORECASE),
    "Mus musculus": re.compile(
        "mouse|mice",
        re.IGNORECASE,
    ),
    "Nicotiana tabacum": re.compile("tobacco", re.IGNORECASE),
    "Oryctolagus cuniculus": re.compile("Oryctolagus.cuniculus|rabbits", re.IGNORECASE),
    "Oryza sativa": re.compile("rice|oryza.sativa|Nipponbare", re.IGNORECASE),
    "Ovis aries": re.compile("Ovis.aries|sheep", re.IGNORECASE),
    "Rattus norvegicus": re.compile("Rattus.norvegicus|rat", re.IGNORECASE),
    "Solanum lycopersicum": re.compile("Solanum.lycopersicum|tomato", re.IGNORECASE),
    "Solanum tuberosum": re.compile("Solanum.tuberosum|potato", re.IGNORECASE),
    "Sus scrofa": re.compile("pigs|piglet|pig|swine", re.IGNORECASE),
    "Triticum aestivum": re.compile("Triticum.aestivum|wheat", re.IGNORECASE),
    "Xenopus tropicalis": re.compile(
        "Xenopus.tropicalis|X. tropicalis|Xenopus", re.IGNORECASE
    ),
}

SPECIES_CONF = {
    "upper": (
        "Arabidopsis thaliana",
        "Bos taurus",
        "Brassica rapa",
        "Callithrix jacchus",
        "Canis lupus familiaris",
        "Capra hircus",
        "Cucumis melo",
        "Felis catus",
        "Gallus gallus",
        "Glycine max",
        "Homo sapiens",
        "Oryctolagus cuniculus",
        "Ovis aries",
        "Sus scrofa",
    ),
    "capitalize": (
        "Apis mellifera",
        "Mesocricetus auratus",
        "Mus musculus",
        "Rattus norvegicus",
    ),
    "lower": (
        "Caenorhabditis elegans",
        "Danio rerio",
    ),
}


# Download gene2pubmed from ftp site to the local data directory
# download_gene2pubmed()
# # gunzip gene2pubmed
# source_file = "../data/gene2pubmed.gz"
# command = ["gunzip", source_file]
# time.sleep(1)
# subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# print("gene2pubmed is downloaded in the local data directory")

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")
df_g2p = pd.read_csv("../data/gene2pubmed", sep="\t")
df_pubdetails = pd.read_csv(f"../data/{date}/{date}_pubdetails.csv", sep=",")
pmids = df_pubdetails["pmid"].tolist()

nomesh_pmid = []
pmids = [str(i) for i in pmids]
print("the total number of pmids :{}".format(len(pmids)))


data_list = []

for pmid in pmids:
    tmp_datalist = []
    species = []
    print(f"\npmid:{pmid}....")
    pmid_row = df_pubdetails[df_pubdetails["pmid"] == int(pmid)]
    pmcid = pmid_row["pmcid"].values[0]
    substances = pmid_row["substances"].values[0]
    mesh = pmid_row["mesh"].values[0]

    # 1. use of MeSH
    substances = ast.literal_eval(substances)
    mesh_list = ast.literal_eval(mesh)

    substances_genes = [s for s in substances if "protein," in s]
    if substances_genes != []:
        print(f"mesh_genes{substances_genes}")
        for mesh_gene in substances_genes:
            splited = mesh_gene.split(",")
            taxname = match_with_csv(
                splited,
                "../csv/corpus_taxonomy.csv",
                "expression",
                "organism_name",
            )
            try:
                splited2 = splited[0].split()
                organism_name = taxname[0]
                taxid = match_with_csv(
                    [organism_name],
                    "../csv/tax_list.csv",
                    "organism_name",
                    "taxid",
                )
                # GeneSymbol in capitalize or uppercase or lowercase depending on taxonomy
                if organism_name in SPECIES_CONF["upper"]:
                    genesymbol = splited2[0].upper()

                elif organism_name in SPECIES_CONF["capitalize"]:
                    genesymbol = splited2[0].capitalize()

                elif organism_name in SPECIES_CONF["lower"]:
                    genesymbol = splited2[0].lower()

                else:
                    genesymbol = splited2[0]
                geneid = match_with_tsv(
                    [genesymbol],
                    f"../gene_ref/{taxname[0]}_genes.tsv",
                    "Symbol",
                    "NCBI GeneID",
                )

                data_list.append(
                    {"#tax_id": taxid[0], "GeneID": geneid[0], "PubMed_ID": pmid}
                )
                tmp_datalist.append(
                    {"#tax_id": taxid[0], "GeneID": geneid[0], "PubMed_ID": pmid}
                )
                print({"#tax_id": taxid[0], "GeneID": geneid[0], "PubMed_ID": pmid})
            except:
                print("MeSH parse error.. Pass.")
                pass

    if mesh_list != []:
        # species = []
        for a_mesh in mesh_list:
            try:
                row = mtree[mtree["mesh"] == a_mesh]
                treeid = row["treeid"].values[0]
                # print(treeid)
                if treeid.startswith("B"):
                    species.append(a_mesh)
            except:
                continue

    # 2. use of PubTator Central if no information from MeSH
    if tmp_datalist == []:
        print("move to pubtator process..")

        if pmcid == "Not found":
            nomesh_pmid.append(pmid)
            print("No pmcid. Added pmid to nomesh_pmid. Processing later..")

        else:
            ptc_genes = []
            ptc_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids={pmcid}"
            # print(ptc_url)
            try:
                tree_ptc = use_eutils(ptc_url)
            except:
                print(f"pubtator api error at {ptc_url}")

            if not tree_ptc.find("./document"):
                nomesh_pmid.append(pmid)
                print(
                    "No document in ptc. Added pmid to nomesh_pmid. Processing later.."
                )

            else:
                try:
                    genes, species_ptc = get_annotations_ptc(tree_ptc)
                    genes_count = collections.Counter(genes).most_common(20)
                    print(f"genes_count:{genes_count}")
                    for gene_count in genes_count:
                        # Extraction of genes that have been text mined more than 5 times from RESULTS or ABSTRACT
                        if gene_count[1] > 15:
                            ptc_genes.append(gene_count[0])
                    print(f"ptc_genes:{ptc_genes}")
                    species_count = collections.Counter(species_ptc).most_common(20)
                    print(f"species_count:{species_count}")
                    for specie_count in species_count:
                        # Extraction of genes that have been text mined more than 10 times from METHODS or ABSTRACT
                        if specie_count[1] > 10:
                            species.append(specie_count[0])
                except:
                    print("fail at parsing ptc...")

                species_str = ",".join(species)
                print(f"species_str:{species_str}_ptc_part")

                organism_names = []
                for tax_pattern in tax_patterns.items():
                    if tax_pattern[1].search(species_str):
                        print(tax_pattern[1].search(species_str))
                        organism_names.append(tax_pattern[0])
                    else:
                        pass

                organism_names = list(set(organism_names))
                print(f"organism_names:{organism_names}")

                for organism_name in organism_names:
                    taxid = match_with_csv(
                        [organism_name],
                        "../csv/tax_list.csv",
                        "organism_name",
                        "taxid",
                    )
                    if organism_name in SPECIES_CONF["capitalize"]:
                        print("capitalize section")
                        genesymbols = match_with_tsv_capitalize(
                            ptc_genes,
                            f"../gene_ref/{organism_name}_genes.tsv",
                            "Symbol",
                            "Symbol",
                        )

                    elif organism_name in SPECIES_CONF["upper"]:
                        print("upper section")
                        genesymbols = match_with_tsv_upper(
                            ptc_genes,
                            f"../gene_ref/{organism_name}_genes.tsv",
                            "Symbol",
                            "Symbol",
                        )

                    elif organism_name in SPECIES_CONF["lower"]:
                        print("lower section")
                        # print(entities_result_nn)
                        genesymbols = match_with_tsv_lower(
                            ptc_genes,
                            f"../gene_ref/{organism_name}_genes.tsv",
                            "Symbol",
                            "Symbol",
                        )

                    else:
                        print("section else")
                        print(f"../gene_ref/{organism_name}_genes.tsv")
                        # print(entities_results)
                        print(ptc_genes)
                        genesymbols = match_with_tsv(
                            ptc_genes,
                            f"../gene_ref/{organism_name}_genes.tsv",
                            "Symbol",
                            "Symbol",
                        )

                    if genesymbols == []:
                        print("no pre-genesymbols")
                        data_list.append(
                            {
                                "#tax_id": taxid[0],
                                "GeneID": "NotFound",
                                "PubMed_ID": pmid,
                            }
                        )
                        print(
                            {
                                "#tax_id": taxid[0],
                                "GeneID": "NotFound",
                                "PubMed_ID": pmid,
                            }
                        )
                    else:
                        genesymbols = list(set(genesymbols))
                        print(f"genesymbols{genesymbols}")
                        try:
                            for genesymbol in genesymbols:
                                geneid = match_with_tsv(
                                    [genesymbol],
                                    f"../gene_ref/{organism_name}_genes.tsv",
                                    "Symbol",
                                    "NCBI GeneID",
                                )
                                data_list.append(
                                    {
                                        "#tax_id": taxid[0],
                                        "GeneID": geneid[0],
                                        "PubMed_ID": pmid,
                                    }
                                )
                                print(
                                    {
                                        "#tax_id": taxid[0],
                                        "GeneID": geneid[0],
                                        "PubMed_ID": pmid,
                                    }
                                )
                        except:
                            print("geneid not found")
                            data_list.append(
                                {
                                    "#tax_id": taxid[0],
                                    "GeneID": "NotFound",
                                    "PubMed_ID": pmid,
                                }
                            )
                            print(
                                {
                                    "#tax_id": taxid[0],
                                    "GeneID": "NotFound",
                                    "PubMed_ID": pmid,
                                }
                            )

print(f"The number of nomesh_pmid: {len(nomesh_pmid)}")
print(f"The list of nomesh_pmids_list: {nomesh_pmid}")
# 3. use of PubTator if no information from MeSH and PubTator Central
# 100 PMIDs for each access in PubTator
list_of_chunked_pmids = generate_chunked_id_list(nomesh_pmid, 100)
for a_chunked_pmids in list_of_chunked_pmids:
    pmids_str = ",".join(a_chunked_pmids)
    pt_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids={pmids_str}"
    # print(pt_url)
    try:
        tree_pubtator = use_eutils(pt_url)
    except:
        print(f"pubtator api error at {pt_url}")

    for element in tree_pubtator.findall("./document"):
        pmid = element.find("id").text
        print(f"\npmid:{pmid}....")
        species = pubtator_species_from_pmid(element)
        genes = pubtator_genes_from_pmid(element)
        species_str = ",".join(species)
        print(f"species_str:{species_str}_pt_part")

        organism_names = []
        for tax_pattern in tax_patterns.items():
            if tax_pattern[1].search(species_str):
                print(tax_pattern[1].search(species_str))
                organism_names.append(tax_pattern[0])
            else:
                pass

        organism_names = list(set(organism_names))
        print(f"organism_names:{organism_names}")
        for organism_name in organism_names:
            taxid = match_with_csv(
                [organism_name],
                "../csv/tax_list.csv",
                "organism_name",
                "taxid",
            )
            if organism_name in SPECIES_CONF["capitalize"]:
                print("capitalize section")
                genesymbols = match_with_tsv_capitalize(
                    genes,
                    f"../gene_ref/{organism_name}_genes.tsv",
                    "Symbol",
                    "Symbol",
                )

            elif organism_name in SPECIES_CONF["upper"]:
                print("upper section")
                genesymbols = match_with_tsv_upper(
                    genes,
                    f"../gene_ref/{organism_name}_genes.tsv",
                    "Symbol",
                    "Symbol",
                )

            elif organism_name in SPECIES_CONF["lower"]:
                print("lower section")
                genesymbols = match_with_tsv_lower(
                    genes,
                    f"../gene_ref/{organism_name}_genes.tsv",
                    "Symbol",
                    "Symbol",
                )

            else:
                print("section else")
                print(genes)
                genesymbols = match_with_tsv(
                    genes,
                    f"../gene_ref/{organism_name}_genes.tsv",
                    "Symbol",
                    "Symbol",
                )

            if genesymbols == []:
                print("no genesymbols found")
                data_list.append(
                    {
                        "#tax_id": taxid[0],
                        "GeneID": "NotFound",
                        "PubMed_ID": pmid,
                    }
                )
                print(
                    {
                        "#tax_id": taxid[0],
                        "GeneID": "NotFound",
                        "PubMed_ID": pmid,
                    }
                )
            else:
                genesymbols = list(set(genesymbols))
                print(f"genesymbols{genesymbols}")
                try:
                    for genesymbol in genesymbols:
                        geneid = match_with_tsv(
                            [genesymbol],
                            f"../gene_ref/{organism_name}_genes.tsv",
                            "Symbol",
                            "NCBI GeneID",
                        )
                        data_list.append(
                            {
                                "#tax_id": taxid[0],
                                "GeneID": geneid[0],
                                "PubMed_ID": pmid,
                            }
                        )
                        print(
                            {
                                "#tax_id": taxid[0],
                                "GeneID": geneid[0],
                                "PubMed_ID": pmid,
                            }
                        )
                except:
                    print("geneid not found (pt_part)")
                    data_list.append(
                        {
                            "#tax_id": taxid[0],
                            "GeneID": "NotFound",
                            "PubMed_ID": pmid,
                        }
                    )
                    print(
                        {
                            "#tax_id": taxid[0],
                            "GeneID": "NotFound",
                            "PubMed_ID": pmid,
                        }
                    )


df_new = pd.DataFrame(data=data_list)
print(df_new)
df_g2p_updated = pd.concat([df_g2p, df_new])
df_g2p_updated.to_csv(f"../data/{date}/{date}_g2p_updated.csv")


# Use Module01LogRead.py to read metadata from the log in a case script was somehow stopped in the middle.
