import json
import sqlite3
import pandas as pd
import datetime

# t_delta = datetime.timedelta(hours=9)
# JST = datetime.timezone(t_delta, "JST")
# now = datetime.datetime.now(JST)
# date = now.strftime("%Y%m%d")
date = "20221215"

connection = sqlite3.connect("../data/gem.db")
cursor = connection.cursor()
cursor.execute(
    "Create table pmid_getools (pmid Text, getools Text, pubtitle Text, bioproid Text, RNA_seq Text, vector Text, cellline Text, editing_type Text, tissue Text, Mutation_type Text)"
)

traffic = json.load(open(f"../csv_gitignore/{date}_pmid_getools.json"))
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

connection.commit()
connection.close()


