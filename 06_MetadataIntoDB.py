import json
import sqlite3
import pandas as pd
import config

connection = sqlite3.connect("./data/gem.db")
cursor = connection.cursor()
cursor.execute(f'drop table if exists {config.sql_table_name};')
cursor.execute(
    f"Create table {config.sql_table_name}(getool Text, pmid Integer, pubtitle Text, pubdate Text, organism_name Text, taxonomy_category Text, genesymbol Text, biopro_id Text, RNA_seq Text, cellline_tissue Text, Mutation_type Text, disease Text)"
)

metadata_json = json.load(open(config.PATH["metadata"]))
print(f"length:{len(metadata_json)}")
columns = [
    "getool",
    "pmid",
    "pubtitle",
    "pubdate",
    "organism_name",
    "taxonomy_category",
    "genesymbol",
    "biopro_id",
    "RNA_seq",
    "cellline_tissue",
    "Mutation_type",
    "disease"
]

for row in metadata_json:
    keys = tuple(row[c] for c in columns)
    cursor.execute(f"insert into {config.sql_table_name} values(?,?,?,?,?,?,?,?,?,?,?,?)", keys)


# make another database called fig2 (species,count)
rs = cursor.execute(f"select distinct organism_name from {config.sql_table_name}")
pre_species_list = rs.fetchall()
species_list = []
for x in pre_species_list:
    species_list.append(x[0])

cursor.execute('drop table if exists fig2;')
cursor.execute("create table if not exists fig2 (taxonomyname Text, entries Integer)")

for species in species_list:
    try:
        rs = cursor.execute(f"select count(*) from {config.sql_table_name} where organism_name = '{species}'")
    except:
        print(f"syntax error at {species}")
        continue

    count = rs.fetchone()[0]
    q = "insert into fig2 (taxonomyname, entries) values ('{}','{}')".format(species,count)

    cursor.execute(q)

connection.commit()
connection.close()

