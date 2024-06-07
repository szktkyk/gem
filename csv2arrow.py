import polars as pl

df = pl.read_csv("./data/csv_gitignore/20240607_ge_metadata_all.csv")
df = df.with_columns(df["pmid"].cast(pl.Utf8))
df.write_ipc("output.arrow")