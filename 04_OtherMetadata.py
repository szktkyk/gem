import ast
import sqlite3
from modules import functions04
import pandas as pd
import config
import csv

DATABASE = "./data/gem.db"
con = sqlite3.connect(DATABASE)

def parse_part1(pmid, con):
    mesh_cur = con.execute(f"select mesh from tmp_pubdetails where pmid = '{pmid}'")
    mesh = mesh_cur.fetchone()[0]
    mesh_list = ast.literal_eval(mesh)
    cellline = []
    tissue = []
    mutation = []
    for a_mesh in mesh_list:
        cur = con.execute(f"select mesh_number from mtree where mesh_term = '{a_mesh}'")
        rs = cur.fetchone()
        if rs == None:
            print(f"error at obtaining treeid for {a_mesh}")
            continue
        else:
            treeid = rs[0]
        # print(treeid)
        # TODO mesh番号正しいかを再確認する
        if treeid.startswith("A11") and len(treeid.split('.')) > 1:
            cellline.append(a_mesh)
        if treeid.startswith("A10") and len(treeid.split('.')) > 1:
            tissue.append(a_mesh)
        if treeid.startswith("G05.365.590") and len(treeid.split('.')) > 3:
            mutation.append(a_mesh)

    cellline_str = ",".join(cellline)
    if cellline_str == "":
        cellline_str = "NotFound"
    tissue_str = ",".join(tissue)
    if tissue_str == "":
        tissue_str = "NotFound"
    mutation_str = ",".join(mutation)
    if mutation_str == "":
        mutation_str = "NotFound"

    return cellline_str, tissue_str, mutation_str

def parse_part2(pmid, pmcid, con):
    if pmcid == "Not found":
        print("pmcid not found")
        abstract_cur = con.execute(f"select abstract from tmp_pubdetails where pmid = '{pmid}'")
        abstract = abstract_cur.fetchone()[0]
        bioproid_list = functions04.parse_bioproid(abstract)
        # addgene = functions04.parse_addgene(abstract, "/Users/suzuki/gem/csv/addgene_vector2.csv")
        geoid_list = functions04.parse_geo(abstract)
    else:
        try:
            tree = functions04.get_xml_from_pmcid(pmcid)
            dataavailability_list = functions04.parse_section_pmc(tree, "SUPPL")
            dataavailability_str = ",".join(dataavailability_list)
            methods_list = functions04.parse_section_pmc(tree, "METHODS")
            methods_str = ",".join(methods_list)
            bioproid_method = functions04.parse_bioproid(methods_str)
            bioproid_suppl = functions04.parse_bioproid(dataavailability_str)
            bioproid_list = list(set(bioproid_method + bioproid_suppl))
            # TODO addgeneをどうするか考える
            # addgene = parse_addgene(
            #     methods_str, "/Users/suzuki/gem/csv/addgene_vector2.csv"
            # )
            geoid_method = functions04.parse_geo(methods_str)
            geoid_suppl = functions04.parse_geo(dataavailability_str)
            geoid_list = list(set(geoid_method + geoid_suppl))
        except:
            print("pmcid is not open to reuse...")
            bioproid_list = []
            geoid_list = []

    return bioproid_list, geoid_list #, addgene, 


def main():
    pmids_cur = con.execute("select pmid from tmp_pubdetails")
    pmids = pmids_cur.fetchall()
    print(f"the number of pmids are {len(pmids)}")
    othermetadata_list = []
    for x in pmids:
        pmid = x[0]
        print(f"\npmid....: {pmid}")
        try:
            cellline_str, tissue_str, mutation_str = parse_part1(pmid, con)
        except:
            print("parse_part1 error. loop continue..")
            cellline_str = "NotFound"
            tissue_str = "NotFound"
            mutation_str = "NotFound"
            pass 

        pmcid_cur = con.execute(f"select pmcid from tmp_pubdetails where pmid = '{pmid}'")
        pmcid = pmcid_cur.fetchone()[0]
        try:
            bioproid_list, geoid_list = parse_part2(pmid, pmcid, con)
        except:
            print("parse_part2 error. loop continue..")
            bioproid_list = []
            geoid_list = []
            pass
        # ID関連の処理
        if len(bioproid_list) == 1:
            id = bioproid_list[0]
            bioproid = f"[{id}](https://www.ncbi.nlm.nih.gov/bioproject/?term={id})"

        elif len(bioproid_list) == 0:
            bioproid = "NotFound"

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
            geoid = "NotFound"

        else:
            pre_list = []
            for id in bioproid_list:
                data = f"[{id}](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={id})"
                pre_list.append(data)
            geoid = ",".join(pre_list)
        
        metadata = {
            "pmid": pmid,
            # "taxonomy_category": taxonomy_category_str,
            "biopro_id": bioproid,
            "RNA_seq": geoid,
            # "vector": addgene,
            "cellline": cellline_str,
            "tissue": tissue_str,
            "Mutation_type": mutation_str,
        }
        print(metadata)
        othermetadata_list.append(metadata)
    
    field_name = [
        "pmid",
        # "taxonomy_category",
        "biopro_id",
        "RNA_seq",
        "cellline",
        "tissue",
        "Mutation_type"
    ]
    with open(
        f"./csv_gitignore/{config.date}_othermetadata.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(othermetadata_list)



if __name__ == "__main__":
    main()