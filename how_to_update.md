# How to update GEM

1. Update following sqlite dbs annually.
    - [meshtree](https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/) with [DB2_MeshTree.py](https://github.com/szktkyk/gem/blob/main/modules/DB2_MeshTree.py) 
    - [taxonomy](https://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/) with [DB4_Taxonomy](https://github.com/szktkyk/gem/blob/main/modules/DB4_Taxonomy.py) 
    - [taxidlineage](https://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/) with [DB10_taxidlineage.py]()

2. Update following sqlite dbs monthly.
    - [GeneInfo](https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz) with [DB1_GeneInfo.py](https://github.com/szktkyk/gem/blob/main/modules/DB1_GeneInfo.py)
    - [gene2pubmed](https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz) with [DB3_g2p.py](https://github.com/szktkyk/gem/blob/main/modules/DB3_g2p.py)

3. Update sqlite index for geneinfo with each taxonomy ([CreateIndex.py](https://github.com/szktkyk/gem/blob/main/modules/CreateIndex.py))

4. Obtain publication details and store it into the sqlite db
    - [W01_Pubdetails.py](https://github.com/szktkyk/gem/blob/main/modules/W01_Pubdetails.py)
    - [DB7_Pubdetails.py](https://github.com/szktkyk/gem/blob/main/modules/DB7_Pubdetails.py)

5. Update gene2pubmed and store it into the sqlite db
    - [W02_UpdateGene2pubmed_new.py]()
    - [W03_Modifyg2p.sh](https://github.com/szktkyk/gem/blob/main/modules/W03_Modifyg2p.sh)
    - [DB5_UpdatedG2p.py](https://github.com/szktkyk/gem/blob/main/modules/DB5_UpdatedG2p.py)

6. Create genome editing related metadata and store them into the sqlite db
    - [W04_CreateMetadata.py](https://github.com/szktkyk/gem/blob/main/modules/W04_CreateMetadata.py)
    - [W05_MetadataIntoDB.py](https://github.com/szktkyk/gem/blob/main/modules/W05_MetadataIntoDB.py)

7. Move the sqlite db (gem.db) and ge_metadata.csv to the server.



