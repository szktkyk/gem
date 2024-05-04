import collections
from modules import ncbi_datasets as nd

def match_genes_species(tmp_genes,tmp_species, pmid):
    extracted_genes = []
    # 3-3. 遺伝子と生物種について処理
    tmp_genes = list(set(tmp_genes))  
    tmp_species = [str(x) for x in tmp_species]      

    # 生物種はカウント順に並べ替える
    species_counts = collections.Counter(tmp_species).most_common(15)
    print(f"species_count:{species_counts}")
    tmp_species = []
    for species_count in species_counts:
        tmp_species.append(species_count[0])
    
    print(f"tmp_species (arranged in order of count):{tmp_species}")

    # 遺伝子と生物種のマッチング
    for a_gene in tmp_genes:
        # print(a_gene)
        taxid = nd.get_taxid_from_geneid(a_gene)
        if taxid in tmp_species:
            extracted_genes.append({"pmid":pmid,"species": taxid, "gene": a_gene})
            print({"pmid":pmid,"species": taxid, "gene": a_gene})
        else:
            continue
    
    return extracted_genes, tmp_species

    # # もし何もマッチしない場合は生物種のみエントリーに含める
    # if extracted_genes == [] and tmp_species != []:
    #     extracted_genes.append({"pmid":pmid,"species": tmp_species[0], "gene": "NotFound"})
    #     tmp2.append({"pmid":pmid,"species": tmp_species[0], "gene": "NotFound"})
    #     print({"pmid":pmid,"species": tmp_species[0], "gene": "NotFound"})
    #     try:
    #         extracted_genes.append({"pmid":pmid,"species": tmp_species[1], "gene": "NotFound"})
    #         tmp2.append({"pmid":pmid,"species": tmp_species[1], "gene": "NotFound"})
    #         print({"pmid":pmid,"species": tmp_species[1], "gene": "NotFound"})
    #     except:
    #         print("Only one taxonomy obtained in the tmp_species. next loop..")
    #         continue     
    
    # if tmp2 != []:
    #     print("tmp2 is not empty. next loop..")
    #     continue
    # # エントリーが何もなければ後ほどEXTRACT2.0で処理する
    # else:
    #     go_to_extract.append(pmid)
    #     print("no species or genes found for this pmid. PMID added for EXTRACT2.0. next loop..")  
    #     continue