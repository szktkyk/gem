import json
import sqlite3
import pandas as pd
from Module0 import *
import re
import datetime
from ModulesForW05 import *
import ast

date = "20230125"
connection = sqlite3.connect("../data/gem.db")
cursor = connection.cursor()
cursor.execute(
    f"Create table metadata{date} (getool Text, pmid Text, pubtitle Text, pubdate Text, taxonomy_category Text, organism_name Text, genesymbol Text,  editing_type Text, gene_counts Integer, biopro_id Text, RNA_seq Text, vector Text, cellline Text, tissue Text, Mutation_type Text)"
)

traffic = json.load(open(f"../data/{date}_joined_metadata.json"))
print(f"length:{len(traffic)}")
columns = [
    "getool",
    "pmid",
    "pubtitle",
    "pubdate",
    "taxonomy_category",
    "organism_name",
    "genesymbol",
    "editing_type",
    "gene_counts",
    "biopro_id",
    "RNA_seq",
    "vector",
    "cellline",
    "tissue",
    "Mutation_type",
]

for row in traffic:
    keys = tuple(row[c] for c in columns)
    cursor.execute(f"insert into metadata{date} values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", keys)
    # print(f'{row["pubmed_id"]} data inserted Succefully')

rs = cursor.execute(f"select distinct organism_name from metadata{date}")
pre_species_list = rs.fetchall()
species_list = []
for x in pre_species_list:
    species_list.append(x[0])

# print(species_list)
# for a in species_list:
#     print(a)
# exit()

cursor.execute(f"create table if not exists fig2 (taxonomyname Text, entries Integer)")

for specie in species_list:
    try:
        rs = cursor.execute(f"select count(*) from metadata{date} where organism_name = '{specie}'")
    except:
        print(f"syntax error at {specie}")
        continue
    # with open("../csv_gitignore/out.csv","wb") as csv_file:
    #     csv
    count = rs.fetchone()[0]
    q = "insert into fig2 (taxonomyname, entries) values ('{}','{}')".format(specie,count)
    # print(q)
    cursor.execute(q)


cur = cursor.execute(f"select distinct pmid from metadata{date}")
rs = cur.fetchall()
# print(rs)

getool_order = {
    "CRISPR-Cas9": 0,
    "TALEN": 1,
    "ZFN": 2,
    "CRISPR-Cas12": 3,
    "CRISPR-Cas3": 4,
    "Base editor": 5,
    "Prime editor": 6,
}
getools = []
for tuplepmid in rs:
    pmid = tuplepmid[0]
    # print(type(pmid))

    cur2 = cursor.execute(
        "select getool from metadata{} where pmid ='{}'".format(date, pmid)
    )
    rs2 = cur2.fetchall()
    tmp = []
    for tuplegetools in rs2:
        tmp.append(tuplegetools[0])
    tmp = set(list(tmp))
    tmp = sorted(tmp, key=lambda x: getool_order[x])
    tmp_str = ",".join(tmp)
    # print(tmp_str)
    cur3 = cursor.execute(f"select pubtitle from metadata{date} where pmid = '{pmid}'")
    pubtitle = cur3.fetchone()[0]
    cur4 = cursor.execute(f"select biopro_id from metadata{date} where pmid = '{pmid}'")
    bioproid = cur4.fetchone()[0]
    cur5 = cursor.execute(f"select RNA_seq from metadata{date} where pmid = '{pmid}'")
    RNA_seq = cur5.fetchone()[0]
    cur6 = cursor.execute(f"select vector from metadata{date} where pmid = '{pmid}'")
    vector = cur6.fetchone()[0]
    cur7 = cursor.execute(f"select cellline from metadata{date} where pmid = '{pmid}'")
    cellline = cur7.fetchone()[0]
    cur8 = cursor.execute(f"select editing_type from metadata{date} where pmid = '{pmid}'")
    editing_type = cur8.fetchone()[0]
    cur9 = cursor.execute(f"select tissue from metadata{date} where pmid = '{pmid}'")
    tissue = cur9.fetchone()[0]
    cur10 = cursor.execute(
        f"select Mutation_type from metadata{date} where pmid = '{pmid}'"
    )
    Mutation_type = cur10.fetchone()[0]

    getools.append(
        {
            "pmid": pmid,
            "getools": tmp_str,
            "pubtitle": pubtitle,
            "bioproid": bioproid,
            "RNA_seq": RNA_seq,
            "vector": vector,
            "cellline": cellline,
            "editing_type": editing_type,
            "tissue": tissue,
            "Mutation_type": Mutation_type,
        }
    )
    # # print(tmp_str)

with open(
    f"../data/{date}_pmid_getools.json", "w"
) as f:
    json.dump(getools, f, indent=3)

cursor.execute(
    "Create table pmid_getools (pmid Text, getools Text, pubtitle Text, bioproid Text, RNA_seq Text, vector Text, cellline Text, editing_type Text, tissue Text, Mutation_type Text)"
)

traffic = json.load(open(f"../data/{date}_pmid_getools.json"))
print(f"length:{len(traffic)}")
columns = [
    "pmid",
    "getools",
    "pubtitle",
    "bioproid",
    "RNA_seq",
    "vector",
    "cellline",
    "editing_type",
    "tissue",
    "Mutation_type",
]

for row in traffic:
    keys = tuple(row[c] for c in columns)
    cursor.execute("insert into pmid_getools values(?,?,?,?,?,?,?,?,?,?)", keys)
    # print(f'{row["pubmed_id"]} data inserted Succefully')

# df_metadata = pd.DataFrame(getools)
# df_metadata.to_csv("../20221031_pmid_getools.csv")


connection.commit()
connection.close()

