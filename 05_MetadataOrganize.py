import pandas as pd
import config
import sqlite3
import config
import json

DATABASE = "./data/gem.db"
con = sqlite3.connect(DATABASE)


df_pubdetails = pd.read_csv(config.PATH["pubdetails"], sep=",")
df_gene_annotation = pd.read_csv(config.PATH["gene_annotation"], sep=",")
df_disease_annotation = pd.read_csv(config.PATH["disease_annotation"], sep=",")
df_disease_annotation.disease = df_disease_annotation.disease.fillna("NotFound")
df_tissue_annotation = pd.read_csv(config.PATH["tissue_annotation"], sep=",")
df_othermetadata = pd.read_csv(config.PATH["othermetadata"], sep=",")
df_othermetadata.RNA_seq = df_othermetadata.RNA_seq.fillna("NotFound")


metadata_list = []
pmids = df_pubdetails["pmid"].tolist()
print(f"the number of pmids are {len(pmids)}")
# pmids = ["37301236","30180793","32112663","31597367","36682603","36894036"]
# pmids = ["37483514"]
# pmids = ["34611160","31076628","36871001"]
for pmid in pmids:
    print(f"\npmid:{pmid}.....")
    pmid_row_pubdeitals = df_pubdetails[df_pubdetails["pmid"] == int(pmid)]
    pubdate = pmid_row_pubdeitals["pubdate"].values[0]
    pubtitle = pmid_row_pubdeitals["title"].values[0]
    getool = pmid_row_pubdeitals["getools"].values[0]
    pmid_row_disease = df_disease_annotation[df_disease_annotation["pmid"] == int(pmid)]
    try:    
        diseases = pmid_row_disease["disease"].values[0]
    except:
        diseases = "NotFound"
    pmid_row_othermetadata = df_othermetadata[df_othermetadata["pmid"] == int(pmid)]
    cellline = pmid_row_othermetadata["cellline"].values[0]
    if cellline == "NotFound":
        cellline = ""
    else:
        cellline = cellline
    biopro_id = pmid_row_othermetadata["biopro_id"].values[0]
    RNA_seq = pmid_row_othermetadata["RNA_seq"].values[0]
    tissue1 = pmid_row_othermetadata["tissue"].values[0]
    if tissue1 == "NotFound":
        tissue1 = ""
    else:
        tissue1 = tissue1
    pmid_row_tissue = df_tissue_annotation[df_tissue_annotation["pmid"] == int(pmid)]
    try:
        tissue2 = pmid_row_tissue["tissue"].values[0]
    except:
        tissue2 = ""
    tissue_cellline = tissue1 + tissue2 + cellline
    if tissue_cellline == "":
        tissue_cellline = "NotFound"
    else:
        pass
    Mutation_type = pmid_row_othermetadata["Mutation_type"].values[0]

    pmid_row = df_gene_annotation[df_gene_annotation["pmid"] == int(pmid)]
    genes = pmid_row["gene"].values
    if len(genes) == 0:
        gene = "NotFound"
        a_species = "NotFound"
        taxonomy_category_str = "NotFound"
        metadata = {
                    "getool": getool,
                    "pmid": pmid,
                    "pubtitle": pubtitle,
                    "pubdate": pubdate,
                    "organism_name": a_species,
                    "taxonomy_category": taxonomy_category_str,
                    "genesymbol": gene,
                    "biopro_id": biopro_id,
                    "RNA_seq": RNA_seq,
                    "cellline_tissue": tissue_cellline,
                    "Mutation_type": Mutation_type,
                    "disease": diseases,
                }
        print(metadata)
        metadata_list.append(metadata)
    else:
        genes = list(set(genes))
    # print(genes)
    for gene in genes:
        species_row = pmid_row[pmid_row["gene"] == gene]
        species = species_row["species"].values
        species = list(set(species))
        # print(species)
        for a_species in species:
            try:
                taxidlineage_cur = con.execute(f"select taxids from taxidlineage where id = '{a_species}'")
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
                taxonomy_category_str = ",".join(taxonomy_category)
            except:
                print(f"taxidlineage of {a_species} is not found")
                taxonomy_category_str = "NotFound"
                pass
            metadata = {
                        "getool": getool,
                        "pmid": pmid,
                        "pubtitle": pubtitle,
                        "pubdate": pubdate,
                        "organism_name": a_species,
                        "taxonomy_category": taxonomy_category_str,
                        "genesymbol": gene,
                        "biopro_id": biopro_id,
                        "RNA_seq": RNA_seq,
                        "cellline_tissue": tissue_cellline,
                        "Mutation_type": Mutation_type,
                        "disease": diseases,
                    }
            print(metadata)
            metadata_list.append(metadata)

with open(f"{config.date}_ge_metadata.json", "w") as f:
    json.dump(metadata_list, f, indent=3)
df_metadata = pd.DataFrame(metadata_list)
df_metadata.to_csv(f"{config.date}_ge_metadata.csv")
    



# 1. PMIDごとに処理
# 2. df_gene_annotationから、pmidに対応するgene_idを取得
# 3. 対応する生物種とtaxonomy categoryを取得
# 4. 残りのメタデータを付与