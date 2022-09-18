import json
import sqlite3
import pandas as pd

connection = sqlite3.connect("../data/20220917/20220917_gem.db")
cursor = connection.cursor()
cursor.execute(
    "Create Table if not exists GEM_metadata (getool Text, pmid Text, pubtitle Text, pubdate Text, organism_name Text, genesymbol Text,  editing_type Text, gene_counts Integer, biopro_id Text, RNA_seq Text, vector Text, cellline Text, tissue Text, Mutation_type Text)"
)

traffic = json.load(open("../json/20220917_ge_metadata_2.json"))
print(f"length:{len(traffic)}")
columns = [
    "getool",
    "pmid",
    "pubtitle",
    "pubdate",
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
    cursor.execute("insert into GEM_metadata values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", keys)
    # print(f'{row["pubmed_id"]} data inserted Succefully')

connection.commit()
connection.close()

df = pd.read_json("../json/20220917_ge_metadata_2.json")
df.to_csv("../20220917_ge_metadata.csv")
