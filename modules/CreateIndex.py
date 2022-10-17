import sqlite3 

DATABASE = "../data/gem.db"
con = sqlite3.connect(DATABASE)

# create index
cur = con.cursor()
cur.execute("create index taxidindex on gene_info(tax_id)")

con.commit()
con.close()

# delete index
# cur = con.cursor()
# cur.execute("drop index taxidindex")

# con.commit()
# con.close()