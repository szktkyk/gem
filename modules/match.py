import collections
from modules import ncbi_datasets as nd

def match_genes_species(tmp_genes,tmp_species, pmid):
    """
    match genes and species using ncbi datasets

    Args:
        tmp_genes (list): list of genes
        tmp_species (list): list of species
        pmid (str): pmid

    Returns:
        _type_: _description_
    """
    extracted_genes = []
    tmp_genes = list(set(tmp_genes))  
    tmp_species = [str(x) for x in tmp_species]      

    # order by count of species
    species_counts = collections.Counter(tmp_species).most_common(15)
    print(f"species_count:{species_counts}")
    tmp_species = []
    for species_count in species_counts:
        tmp_species.append(species_count[0])
    
    print(f"tmp_species (arranged in order of count):{tmp_species}")

    # match gene with species
    for a_gene in tmp_genes:
        # print(a_gene)
        taxid = nd.get_taxid_from_geneid(a_gene)
        if taxid in tmp_species:
            extracted_genes.append({"pmid":pmid,"species": taxid, "gene": a_gene})
            print({"pmid":pmid,"species": taxid, "gene": a_gene})
        else:
            continue
    
    return extracted_genes, tmp_species
