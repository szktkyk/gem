import json
import pandas as pd
import re
import datetime
from ModulesForW05 import *
import ast
import sqlite3


DATABASE = "../data/gem.db"
con = sqlite3.connect(DATABASE)

cur = con.execute("select distinct pmid from metadata221017")
rs = cur.fetchall()
# print(rs)

getool_order = {'CRISPR-Cas9': 0, 'TALEN': 1, 'ZFN': 2, 'CRISPR-Cas12': 3, 'CRISPR-Cas3':4, 'Base editor':5, 'Prime editor':6}
getools = []
for tuplepmid in rs:
    pmid = tuplepmid[0]
    # print(type(pmid))

    cur2 = con.execute(f"select getool from metadata221017 where pmid ='{pmid}'")
    rs2 = cur2.fetchall()
    tmp = []
    for tuplegetools in rs2:
        tmp.append(tuplegetools[0])
    tmp = set(list(tmp))
    tmp = sorted(tmp, key=lambda x: getool_order[x])
    tmp_str = ",".join(tmp)
    # print(tmp_str)
    cur3 = con.execute(f"select pubtitle from metadata221017 where pmid = '{pmid}'")
    pubtitle = cur3.fetchone()[0]
    cur4 = con.execute(f"select biopro_id from metadata221017 where pmid = '{pmid}'")
    bioproid = cur4.fetchone()[0]
    cur5 = con.execute(f"select RNA_seq from metadata221017 where pmid = '{pmid}'")
    RNA_seq = cur5.fetchone()[0]
    cur6 = con.execute(f"select vector from metadata221017 where pmid = '{pmid}'")
    vector = cur6.fetchone()[0]
    cur7 = con.execute(f"select cellline from metadata221017 where pmid = '{pmid}'")
    cellline = cur7.fetchone()[0]
    cur8 = con.execute(f"select editing_type from metadata221017 where pmid = '{pmid}'")
    editing_type = cur8.fetchone()[0]
    cur9 = con.execute(f"select tissue from metadata221017 where pmid = '{pmid}'")
    tissue = cur9.fetchone()[0]
    cur10 = con.execute(f"select Mutation_type from metadata221017 where pmid = '{pmid}'")
    Mutation_type = cur10.fetchone()[0]


    getools.append({'pmid':pmid, 'getools':tmp_str,'pubtitle':pubtitle,'bioproid':bioproid,'RNA_seq':RNA_seq,'vector':vector,'cellline':cellline,'editing_type':editing_type,'tissue':tissue,'Mutation_type':Mutation_type})
    # # print(tmp_str)

with open(f"/Users/suzuki/gem/csv_gitignore/20221031_pmid_getools.json", "w") as f:
    json.dump(getools, f, indent=3)

df_metadata = pd.DataFrame(getools)
df_metadata.to_csv("../20221031_pmid_getools.csv")
con.close()