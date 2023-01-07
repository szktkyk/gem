import json
import sqlite3
import pandas as pd
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")


connection = sqlite3.connect("../data/gem.db")
cursor = connection.cursor()
cursor.execute(
    "Create table species_category (pmid Text, species_category Text)"
)

traffic = json.load(open(f"../csv_gitignore/20221116_species_categories.json"))
print(f"length:{len(traffic)}")
columns = [
    "pmid",
    "species_category"
]

for row in traffic:
    keys = tuple(row[c] for c in columns)
    cursor.execute("insert into species_category values(?,?)", keys)
    # print(f'{row["pubmed_id"]} data inserted Succefully')

connection.commit()
connection.close()


