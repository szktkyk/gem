import ast
import polars as pl
import config
import csv
import sqlite3
from modules import parsing, read_log, check_results

con = sqlite3.connect("./data/gem.db")

def parse_part1(pmid, df_row, con):
    # MeSH
    mesh = df_row["mesh"][0]          
    mesh_list = ast.literal_eval(mesh)

    # cellline, tissue, mutation, disease from MeSH
    cellline = []
    tissue = []
    mutation = []
    disease = []
    for a_mesh in mesh_list:
        cur = con.execute("select mesh_number from mtree where mesh_term = ?", (a_mesh,))
        rs = cur.fetchone()
        if rs == None:
            print(f"error at obtaining treeid for {a_mesh}")
            continue
        else:
            treeid = rs[0]
        if treeid.startswith("A11") and len(treeid.split('.')) > 1:
            cellline.append(a_mesh)
        if treeid.startswith("A10") and len(treeid.split('.')) > 1:
            tissue.append(a_mesh)
        if treeid.startswith("G05.365.590") and len(treeid.split('.')) > 3:
            mutation.append(a_mesh)
        if treeid.startswith("C23.550.288") and len(treeid.split('.')) > 3:
            disease.append(a_mesh)

    mutation_str = ",".join(mutation)
    if mutation_str == "":
        mutation_str = "NotFound"

    return cellline, tissue, mutation_str, disease


def parse_part2(pmcid, df_row):
    # getool
    getool = df_row["getools"][0]
    getool_list = ast.literal_eval(getool)
    
    if pmcid == "Not found":
        print("pmcid not found")
        # Only abstract is available
        abstract = df_row["abstract"][0]
        if type(abstract) == str:
            bioproid_list = parsing.parse_bioproid(abstract)
            geoid_list = parsing.parse_geo(abstract)
        else:
            bioproid_list = []
            geoid_list = []

    else:
        try:
            tree = parsing.get_xml_from_pmcid(pmcid)
            dataavailability_str = ",".join(parsing.parse_section_pmc(tree, "SUPPL"))
            methods_str = ",".join(parsing.parse_section_pmc(tree, "METHODS"))
            bioproid_method = parsing.parse_bioproid(methods_str)
            bioproid_suppl = parsing.parse_bioproid(dataavailability_str)
            bioproid_list = list(set(bioproid_method + bioproid_suppl))
            # TODO work on ADDGENE???
            # addgene = parse_addgene(
            #     methods_str, "/Users/suzuki/gem/csv/addgene_vector2.csv"
            # )
            geoid_method = parsing.parse_geo(methods_str)
            geoid_suppl = parsing.parse_geo(dataavailability_str)
            geoid_list = list(set(geoid_method + geoid_suppl))
            if getool_list == []:
                getool_list = parsing.parse_getool(methods_str)
            else:
                getool_list = getool_list
        except:
            print("pmcid is not open to use with API...")
            bioproid_list = []
            geoid_list = []

    return bioproid_list, geoid_list, getool_list #, addgene, 


def main():
    df = pl.read_csv(config.PATH["pubdetails"])
    pmids = df["pmid"].to_list()
    print(f"the number of pmids are {len(pmids)}")
      
    othermetadata_list = []
    
    pmids = [str(i) for i in pmids]
    for pmid in pmids:
        print(f"\npmid....: {pmid}")
        df_row = df.filter(df["pmid"] == pmid)
        cellline_str, tissue_str, mutation_str, disease_list = parse_part1(pmid, df_row, con)

        pmcid = df_row["pmcid"][0]

        bioproid_list, geoid_list, getool_list = parse_part2(pmcid, df_row)
      
        # related IDs
        bioproid_list = list(set(bioproid_list))
        if bioproid_list == []:
            bioproid = "NotFound"
        else:
            bioproid = ",".join(bioproid_list)
        geoid_list = list(set(geoid_list))
        if geoid_list == []:
            geoid = "NotFound"
        else:  
            geoid = ",".join(geoid_list)
      
        metadata = {
            "pmid": pmid,
            "getool": ",".join(getool_list),
            "biopro_id": bioproid,
            "RNA_seq": geoid,
            "cellline": cellline_str,
            "tissue": tissue_str,
            "mutation_type": mutation_str,
            "disease": disease_list
        }
        print(metadata)
        othermetadata_list.append(metadata)
    
    field_name = [
        "pmid",
        "getool",
        "biopro_id",
        "RNA_seq",
        "cellline",
        "tissue",
        "mutation_type",
        "disease"
    ]
    with open(
        f"./data/csv_gitignore/{config.date}_othermetadata.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(othermetadata_list)


if __name__ == "__main__":
    main()