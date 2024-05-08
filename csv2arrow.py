import polars as pl

df = pl.read_csv("20240507_ge_metadata.csv")
df = df.with_columns(df["pmid"].cast(pl.Utf8))
df.write_ipc("output.arrow")