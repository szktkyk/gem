import json
import sqlite3
import pandas as pd

date = "20221215"
connection = sqlite3.connect("../data/gem.db")
cursor = connection.cursor()
cursor.execute(
    f"Create table metadata{date} (getool Text, pmid Text, pubtitle Text, pubdate Text, taxonomy_category Text, organism_name Text, genesymbol Text,  editing_type Text, gene_counts Integer, biopro_id Text, RNA_seq Text, vector Text, cellline Text, tissue Text, Mutation_type Text)"
)

traffic = json.load(open(f"../csv_gitignore/{date}_ge_metadata.json"))
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
    cursor.execute("insert into metadata20221215 values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", keys)
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

cursor.execute("create table if not exists fig2 (taxonomyname Text, entries Integer)")

for specie in species_list:
    try:
        rs = cursor.execute(f"select count(*) from metadata221017 where organism_name = '{specie}'")
    except:
        print(f"syntax error at {specie}")
        continue
    # with open("../csv_gitignore/out.csv","wb") as csv_file:
    #     csv
    count = rs.fetchone()[0]
    q = "insert into fig2 (taxonomyname, entries) values ('{}','{}')".format(specie,count)
    # print(q)
    cursor.execute(q)
    
connection.commit()
connection.close()

# df = pd.read_json("../csv_gitignore/20221014_ge_metadata.json")
# df.to_csv("../20221017_metadata.csv")
