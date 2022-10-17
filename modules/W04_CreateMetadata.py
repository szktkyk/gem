import json
import pandas as pd
import re
import datetime
from ModulesForW05 import *
import ast
import sqlite3

DATABASE = "../data/gem.db"
con = sqlite3.connect(DATABASE)

parse_patterns = {
    "CRISPR-Cas9": re.compile("CRISPR.Cas9|\scas9|spcas9", re.IGNORECASE),
    "TALEN": re.compile(
        "TALEN|transciption.activator.like.effector.nuclease", re.IGNORECASE
    ),
    "ZFN": re.compile("ZFN|zinc.finger.nuclease", re.IGNORECASE),
    "Base editor": re.compile("Base.edit", re.IGNORECASE),
    "Prime editor": re.compile("Prime.Edit", re.IGNORECASE),
    "CRISPR-Cas3": re.compile("CRISPR.Cas3", re.IGNORECASE),
    "CRISPR-Cas12": re.compile("CRISPR.Cas12", re.IGNORECASE),
    # PITChは手法なので不適切。
    # "PITCh": re.compile("PITCh"),
    # 今の場合はなしでも良いかも
    # "SaCas9": re.compile("SaCas9|KKH.SaCas9", re.IGNORECASE),
    # knock-downは未対応なのでこれは保留 "CRISPR-Cas13": re.compile("CRISPR.Cas13", re.IGNORECASE),
}


def parse_part1(pmid, df_pubdetails):
    pmid_row = df_pubdetails[df_pubdetails["pmid"] == int(pmid)]
    pubdate = pmid_row["pubdate"].values[0]
    pubtitle = pmid_row["title"].values[0]
    pmcid = pmid_row["pmcid"].values[0]
    keywords = pmid_row["keywordlist"].values[0]
    mesh = pmid_row["mesh"].values[0]
    mesh_list = ast.literal_eval(mesh)
    cellline = []
    tissue = []
    mutation = []
    for a_mesh in mesh_list:
        cur = con.execute(f"select mesh_number from mtree where mesh_term = '{a_mesh}'")
        rs = cur.fetchone()
        if rs == None:
            print(f"error at obtaining treeid for {a_mesh}")
            pass
        else:
            treeid = rs[0]
        # print(treeid)
        if treeid.startswith("A11") and len(treeid.split('.')) > 1:
            cellline.append(a_mesh)
        if treeid.startswith("A10") and len(treeid.split('.')) > 1:
            tissue.append(a_mesh)
        if treeid.startswith("G05.365.590") and len(treeid.split('.')) > 3:
            mutation.append(a_mesh)

    cellline_str = ",".join(cellline)
    if cellline_str == "":
        cellline_str = "Not found"
    tissue_str = ",".join(tissue)
    if tissue_str == "":
        tissue_str = "Not found"
    mutation_str = ",".join(mutation)
    if mutation_str == "":
        mutation_str = "Not found"
    if pmcid == "Not found":
        print("no pmcid...")
        getools = []
        for parse_pattern in parse_patterns.items():
            if parse_pattern[1].search(pubtitle):
                print(parse_pattern[1].search(pubtitle))
                getools.append(parse_pattern[0])

            if parse_pattern[1].search(keywords):
                print(parse_pattern[1].search(keywords))
                getools.append(parse_pattern[0])
        getools = list(set(getools))
        tree = None

    else:
        try:
            tree = get_xml_from_pmcid(pmcid)
            methods_list = parse_section_pmc(tree, "METHODS")
            if methods_list != []:
                print("methods_parsed completed...")
            methods_str = ",".join(methods_list)
            getools = []

            for parse_pattern in parse_patterns.items():
                if parse_pattern[1].search(methods_str):
                    print(parse_pattern[1].search(methods_str))
                    getools.append(parse_pattern[0])

                if parse_pattern[1].search(pubtitle):
                    print(parse_pattern[1].search(pubtitle))
                    getools.append(parse_pattern[0])

                if parse_pattern[1].search(keywords):
                    print(parse_pattern[1].search(keywords))
                    getools.append(parse_pattern[0])
            getools = list(set(getools))
        except:
            print("pmcid is not open to reuse...")
            getools = []
            for parse_pattern in parse_patterns.items():
                if parse_pattern[1].search(pubtitle):
                    print(parse_pattern[1].search(pubtitle))
                    getools.append(parse_pattern[0])

                if parse_pattern[1].search(keywords):
                    print(parse_pattern[1].search(keywords))
                    getools.append(parse_pattern[0])
            getools = list(set(getools))
            tree = None

    return (
        tree,
        pmcid,
        pubdate,
        pubtitle,
        getools,
        cellline_str,
        tissue_str,
        mutation_str,
    )


def parse_part2(pmid, pmcid, df_pubdetails, tree):
    if pmcid == "Not found":
        pmid_row = df_pubdetails[df_pubdetails["pmid"] == int(pmid)]
        abstract = pmid_row["abstract"].values[0]
        keywords = pmid_row["keywordlist"].values[0]
        editing_type1 = parse_editingtype(abstract)
        editing_type2 = parse_editingtype(keywords)
        editing_type = list(set(editing_type1 + editing_type2))
        editing_type_str = ",".join(editing_type)
        if editing_type_str == "":
            editing_type_str = "Not found"
        bioproid_list = parse_bioproid(abstract)
        addgene = parse_addgene(abstract, "/Users/suzuki/gem/csv/addgene_vector2.csv")
        geoid_list = parse_geo(abstract)

    else:
        dataavailability_list = parse_section_pmc(tree, "SUPPL")
        dataavailability_str = ",".join(dataavailability_list)
        results_list = parse_section_pmc(tree, "RESULTS")
        results_str = ",".join(results_list)
        editing_type = parse_editingtype(results_str)
        editing_type_str = ",".join(editing_type)
        if editing_type_str == "":
            editing_type_str = "Not found"
        methods_list = parse_section_pmc(tree, "METHODS")
        methods_str = ",".join(methods_list)
        bioproid_method = parse_bioproid(methods_str)
        bioproid_suppl = parse_bioproid(dataavailability_str)
        bioproid_list = list(set(bioproid_method + bioproid_suppl))
        addgene = parse_addgene(
            methods_str, "/Users/suzuki/gem/csv/addgene_vector2.csv"
        )
        geoid_method = parse_geo(methods_str)
        geoid_suppl = parse_geo(dataavailability_str)
        geoid_list = list(set(geoid_method + geoid_suppl))

    return editing_type_str, bioproid_list, addgene, geoid_list


t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")
# date = "20220820"

path = f"/Users/suzuki/gem/csv_gitignore/{date}_g2p_updated.tsv"
df_gene2pubmed = pd.read_csv(path, sep="\t")
df_pubdetails = pd.read_csv(
    f"/Users/suzuki/gem/data/20221013/20221013_pubdetails.csv", sep=","
)

pmids = df_pubdetails["pmid"].tolist()
print(f"the number of pmids are {len(pmids)}")
ge_metadata = []


for pmid in pmids:
    # parse_part1 and parse_part2
    print(f"\npmid....:{pmid}")
    try:
        cur = con.execute(f"select * from updatedg2p where PubMed_ID = '{pmid}'")
        rows = cur.fetchall()
    except:
        print(f"error at g2p sql search.. loop continue")
        continue
    if rows == []:   
        print("No entry in g2p. loop continue..")
        continue

    else:
        try:
            (
                tree,
                pmcid,
                pubdate,
                pubtitle,
                getools,
                cellline_str,
                tissue_str,
                mutation_str,
            ) = parse_part1(pmid, df_pubdetails)
        except:
            print("parse_part1 error. loop continue..")
            continue
        if getools == []:
            print("getools_list is empty. loop continue..")
            continue
        else:
            try:
                editing_type, bioproid_list, addgene, geoid_list = parse_part2(
                    pmid, pmcid, df_pubdetails, tree
                )
            except:
                print("parse_part2 error. loop continue..")
                continue
        # if the number of row is over 1000, this pmid entry is omitted
        # number_row = len(row.axes[0])
        if len(rows) > 1000:
            print("too many rows (more than 1000). Only the first row is processing")
            taxid = rows[0][0]
            cur2 = con.execute(f"select tax_name from taxonomy where tax_id = '{taxid}'")
            taxname = cur2.fetchone()[0]
            geneid = rows[0][1]
            if geneid != "NotFound":
                geneurl = f"https://www.ncbi.nlm.nih.gov/gene/{geneid}"
                cur3 = con.execute(f"select Symbol from gene_info where GeneID = '{geneid}'")
                genesymbol = cur3.fetchone()[0]
                data_genesymbol = "[{}]({})".format(genesymbol,geneurl)          
                cur4 = con.execute(f"select count(*) from updatedg2p where GeneID = '{geneid}'")
                genecounts = cur4.fetchone()[0]

            else:
                print("fail at getting geneid and genecounts.")
                geneid = "Not found"
                genecounts = None
                data_genesymbol = "Not found"

            if len(bioproid_list) == 1:
                id = bioproid_list[0]
                bioproid = f"[{id}](https://www.ncbi.nlm.nih.gov/bioproject/?term={id})"

            elif len(bioproid_list) == 0:
                bioproid = "Not found"

            else:
                pre_list = []
                for id in bioproid_list:
                    data = f"[{id}](https://www.ncbi.nlm.nih.gov/bioproject/?term={id})"
                    pre_list.append(data)
                bioproid = ",".join(pre_list)

            if len(geoid_list) == 1:
                id = geoid_list[0]
                geoid = (
                    f"[{id}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id})"
                )

            elif len(geoid_list) == 0:
                geoid = "Not found"

            else:
                pre_list = []
                for id in bioproid_list:
                    data = f"[{id}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id})"
                    pre_list.append(data)
                geoid = ",".join(pre_list)

            for getool in getools:
                metadata = {
                    "getool": getool,
                    "pmid": f"[{pmid}](http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid})",
                    "pubtitle": pubtitle,
                    "pubdate": pubdate,
                    "organism_name": taxname,
                    "genesymbol": data_genesymbol,
                    "editing_type": editing_type,
                    "gene_counts": genecounts,
                    "biopro_id": bioproid,
                    "RNA_seq": geoid,
                    "vector": addgene,
                    "cellline": cellline_str,
                    "tissue": tissue_str,
                    "Mutation_type": mutation_str,
                }
                print(metadata)
                ge_metadata.append(metadata)

        else:
            for row in rows:
                taxid = row[0]
                cur2 = con.execute(f"select tax_name from taxonomy where tax_id = '{taxid}'")
                taxname = cur2.fetchone()[0]
                geneid = row[1]
                if geneid != "NotFound":
                    geneurl = f"https://www.ncbi.nlm.nih.gov/gene/{geneid}"
                    cur3 = con.execute(f"select Symbol from gene_info where GeneID = '{geneid}'")
                    genesymbol = cur3.fetchone()[0]     
                    data_genesymbol = "[{}]({})".format(genesymbol,geneurl)       
                    cur4 = con.execute(f"select count(*) from updatedg2p where GeneID = '{geneid}'")
                    genecounts = cur4.fetchone()[0]

                else:
                    print("fail at getting geneid and genecounts.")
                    geneid = "Not found"
                    genecounts = None
                    data_genesymbol = "Not found"

                if len(bioproid_list) == 1:
                    id = bioproid_list[0]
                    bioproid = (
                        f"[{id}](https://www.ncbi.nlm.nih.gov/bioproject/?term={id})"
                    )

                elif len(bioproid_list) == 0:
                    bioproid = "Not found"

                else:
                    pre_list = []
                    for id in bioproid_list:
                        data = f"[{id}](https://www.ncbi.nlm.nih.gov/bioproject/?term={id})"
                        pre_list.append(data)
                    bioproid = ",".join(pre_list)

                if len(geoid_list) == 1:
                    id = geoid_list[0]
                    geoid = f"[{id}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id})"

                elif len(geoid_list) == 0:
                    geoid = "Not found"

                else:
                    pre_list = []
                    for id in bioproid_list:
                        data = f"[{id}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id})"
                        pre_list.append(data)
                    geoid = ",".join(pre_list)

                for getool in getools:
                    metadata = {
                        "getool": getool,
                        "pmid": f"[{pmid}](http://rdf.ncbi.nlm.nih.gov/pubmed/{pmid})",
                        "pubtitle": pubtitle,
                        "pubdate": pubdate,
                        "organism_name": taxname,
                        "genesymbol": data_genesymbol,
                        "editing_type": editing_type,
                        "gene_counts": genecounts,
                        "biopro_id": bioproid,
                        "RNA_seq": geoid,
                        "vector": addgene,
                        "cellline": cellline_str,
                        "tissue": tissue_str,
                        "Mutation_type": mutation_str,
                    }
                    print(metadata)
                    ge_metadata.append(metadata)


# exit()
with open(f"/Users/suzuki/gem/csv_gitignore/{date}_ge_metadata.json", "w") as f:
    json.dump(ge_metadata, f, indent=3)

df_metadata = pd.DataFrame(ge_metadata)
df_metadata.to_csv("../20221013_test_ge_metadata.csv")
