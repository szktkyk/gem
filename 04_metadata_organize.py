import polars as pl
import config
import config
import json
import sqlite3
from modules import ncbi_datasets as nd
import ast
from nltk.stem import PorterStemmer

con = sqlite3.connect("./data/gem.db")
stemmer = PorterStemmer()

df_pubdetails = pl.read_csv(config.PATH["pubdetails"])
df_gene_annotation = pl.read_csv(config.PATH["gene_annotation"])
df_disease_annotation = pl.read_csv(config.PATH["disease_annotation"])
df_tissue_annotation = pl.read_csv(config.PATH["tissue_annotation"])
df_othermetadata = pl.read_csv(config.PATH["othermetadata"])

# df_gene_annotationの重複行を削除する
df_gene_annotation = df_gene_annotation.unique()

metadata_list = []
pmids = df_pubdetails["pmid"].to_list()
print(f"the number of pmids are {len(pmids)}")

for pmid in pmids:
    print(f"\npmid:{pmid}.....")
    # それぞれのdfの行を取得
    pmid_row_pubdeitals = df_pubdetails.filter(df_pubdetails["pmid"] == pmid)
    pmid_row_othermetadata = df_othermetadata.filter(df_othermetadata["pmid"] == pmid)
    pmid_row_disease = df_disease_annotation.filter(df_disease_annotation["pmid"] == pmid)
    pmid_row_tissue = df_tissue_annotation.filter(df_tissue_annotation["pmid"] == pmid)
    pmid_row_gene = df_gene_annotation.filter(df_gene_annotation["pmid"] == pmid)
    if len(pmid_row_gene) >= 2:
        #{'pmid': '38685234', 'species': '7227', 'gene': 'NotFound'}
        #{'pmid': '38685234', 'species': '7227', 'gene': '42795'}
        # 上記みたいなやつのgene:NotFoundを削除する処理
        pmid_row_gene = pmid_row_gene.filter(
        # geneがNotFoundで、speciesが重複しているものを選択する
        (~pl.col("gene").eq("NotFound") & pl.col("species")
        .is_in(pmid_row_gene.filter(pl.col("gene").ne("NotFound"))
                .select("species").unique()))
                )
    else:
        pmid_row_gene = pmid_row_gene


    # 文献情報
    pubdate = pmid_row_pubdeitals["pubdate"][0]
    pubtitle = pmid_row_pubdeitals["title"][0]

    # getoolの情報
    getool = pmid_row_othermetadata["getool"][0]
    if getool == None:
        getool = "NotFound"
    else:
        getool = getool

    # diseaseの情報 
    try:  
        diseases_02 = ast.literal_eval(pmid_row_disease["disease"][0])
    except:
        diseases_02 = []
    diseases_03 = ast.literal_eval(pmid_row_othermetadata["disease"][0])
    diseases = diseases_02 + diseases_03
    if diseases == []:
        diseases_str = "NotFound"
    else:
        # stemmerで語幹に変換
        diseases_stemmed = [stemmer.stem(word) for word in diseases]
        diseases_stemmed = list(set(diseases_stemmed))
        diseases_str = ",".join(diseases_stemmed)
    
    # cellline + tissueの情報
    cellline = ast.literal_eval(pmid_row_othermetadata["cellline"][0])
    tissue1 = ast.literal_eval(pmid_row_othermetadata["tissue"][0])
    try:
        tissue2 = ast.literal_eval(pmid_row_tissue["tissue"][0])
    except:
        tissue2 = []
    tissue_cellline = tissue1 + tissue2 + cellline
    if tissue_cellline == []:
        tissue_cellline_str = "NotFound"
    else:
        # stemmerで語幹に変換
        tissuecellline_stemmed = [stemmer.stem(word) for word in tissue_cellline]
        tissuecellline_stemmed = list(set(tissuecellline_stemmed))
        tissue_cellline_str = ",".join(tissuecellline_stemmed)
    
    # ID関連の情報
    biopro_id = pmid_row_othermetadata["biopro_id"][0]
    RNA_seq = pmid_row_othermetadata["RNA_seq"][0]

    # mutation typeの情報
    mutation_type = pmid_row_othermetadata["mutation_type"][0]

    # geneの情報
    genes = pmid_row_gene["gene"].to_list()
    if len(genes) == 0:
        gene = "NotFound"
        a_species = "NotFound"
        taxonomy_category_str = "NotFound"
        metadata = {
                    "getool": getool,
                    "pmid": str(pmid),
                    "pubtitle": pubtitle,
                    "pubdate": pubdate,
                    "organism_name": a_species,
                    "taxonomy_category": taxonomy_category_str,
                    "genesymbol": gene,
                    "biopro_id": biopro_id,
                    "RNA_seq": RNA_seq,
                    "cellline_tissue": tissue_cellline_str,
                    "mutation_type": mutation_type,
                    "disease": diseases_str,
                }
        print(metadata)
        metadata_list.append(metadata)
    else:
        genes = list(set(genes))
    # print(genes)
    for gene in genes:
        species_row = pmid_row_gene.filter(pmid_row_gene["gene"] == gene)
        species = species_row["species"].to_list()
        species = list(set(species))
        for a_species in species:
            taxidlineage_cur = con.execute(f"select taxids from taxidlineage where id = ?", (a_species,))
            taxidlineage = taxidlineage_cur.fetchone()[0]
            taxonomy_category = []
            if " 8292 " in taxidlineage or a_species == "8292":
                taxonomy_category.append("amphibians")
            if " 8782 " in taxidlineage or a_species == "8782":
                taxonomy_category .append("birds")
            if " 7898 " in taxidlineage or a_species == "7898":
                taxonomy_category.append("fishes")
            if " 40674 " in taxidlineage or a_species == "40674":
                taxonomy_category.append("mammals")
            if " 8504 " in taxidlineage or a_species == "8504":
                taxonomy_category.append("reptiles")
            if " 50557 " in taxidlineage or a_species == "50557":
                taxonomy_category.append("insects")
            if " 2 " in taxidlineage or a_species == "2":
                taxonomy_category.append("bacteria")
            if " 4751 " in taxidlineage or a_species == "4751":
                taxonomy_category.append("fungi")
            if " 3193 " in taxidlineage or a_species == "3193":
                taxonomy_category.append("plants")
            if " 6237 " in taxidlineage or a_species == "6237":
                taxonomy_category.append("nematodes")
            if " 3041 " in taxidlineage or a_species == "3041":
                taxonomy_category.append("green algae")
            if "10239 " in taxidlineage or a_species == "10239":
                taxonomy_category.append("viruses")

            if taxonomy_category == []:
                taxonomy_category_str = "others"
            else:
                taxonomy_category_str = ",".join(taxonomy_category)
            try:
                species_name_cur = con.execute(f"select tax_name from taxonomy where tax_id = ?", (a_species,))
                species_name = species_name_cur.fetchone()[0]
            except:
                species_name = nd.get_taxname_from_taxid(a_species)

            if gene == "NotFound":
                gene_info = "NotFound"
            else:
                try:
                    genesymbol = nd.get_genesymbol_from_geneid(gene)
                    gene_info = f"{genesymbol} (NCBI_GeneID:{gene})"
                except:
                    genesymbol = gene
                    gene_info = f"(NCBI_GeneID:{gene})"
            metadata = {
                        "getool": getool,
                        "pmid": str(pmid),
                        "pubtitle": pubtitle,
                        "pubdate": pubdate,
                        "organism_name": species_name,
                        "taxonomy_category": taxonomy_category_str,
                        "genesymbol": gene_info,
                        "biopro_id": biopro_id,
                        "RNA_seq": RNA_seq,
                        "cellline_tissue": tissue_cellline_str,
                        "mutation_type": mutation_type,
                        "disease": diseases_str,
                    }
            print(metadata)
            metadata_list.append(metadata)

print(f"metadata_list:{len(metadata_list)}")
# getool, gene, speciesが全てNotFoundの行は削除する
new_metadata_list = []
for i in metadata_list:
    if i["getool"] == "NotFound" and i["genesymbol"] == "NotFound" and i["organism_name"] == "NotFound":
        continue
    else:
        new_metadata_list.append(i)
print(f"new_metadata_list:{len(new_metadata_list)}")


with open(f"{config.date}_ge_metadata.json", "w") as f:
    json.dump(new_metadata_list, f, indent=3)
df_metadata = pl.DataFrame(new_metadata_list)
df_metadata.write_csv(f"{config.date}_ge_metadata.csv")
    



# 1. PMIDごとに処理
# 2. df_gene_annotationから、pmidに対応するgene_idを取得
# 3. 対応する生物種とtaxonomy categoryを取得
# 4. 残りのメタデータを付与