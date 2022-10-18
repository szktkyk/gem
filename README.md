# GEM: Genome Editing Meta-database ver1
## What is GEM?
- GEM is the dataset of genome editing related metadata automatically extracted from PubMed articles. Extraction of metadata is achieved by utilizing the following databases. 
    - PubMed
    - PubMed Central
    - NCBI gene
    - PubTator Central
    - MeSH
    - NCBI taxonomy

- `20221017_metadata.csv` is the outcome dataset. The dataset is visualized and searchable in your localhost if you execute `app.py`.


## How to use interface in your local environment 
1. install miniconda
2. move to the gem directory
3. `conda create -n gemenv --file env_name_intel.txt`
4. `conda activate gemenv`
5. `python app.py` to start the web application in your localhost.


## Used data for metadata collection
- gene_info.gz (https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz) (downloaded at 2022-Oct-12)
- gene2pubmed (https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2pubmed.gz) (downloaded at 2022-Oct-12)
- mtrees2022.bin (https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/meshtrees/mtrees2022.bin) (downloaded at 2022-Oct-12)
- new_taxdump (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) (downloaded at 2022-Jun-28)
- PubTator central (used in calculation between 2022-Oct-14 - 2022-Oct-16)


## if you want to make your own dataset
1. Write searching terms in pubmed_terms in `W01_Pubdetails.py`.
2. Build DB by executing from `DB1_Geneinfo.py` to `DB4_Taxonomy.py`
3. `python W01_Pubdetails.py`
4. Insert pubdetails into DB by executing `DB7_Pubdetails.py`
5. `python W02_Update_Gene2pubmed.py`
6. `sh W03_Modifyg2p.sh`
7. Insert updated gene2pubmed into DB by executing `DB6_Metadata.py`
8. `python W05_CreateMetadata.py` to get the csv file containing metadata.
9. Insert metadata into DB by executing `W05_MetadataIntoDB.py`
10. Write a path to csv file in `app.py`.
11. `python app.py` to see the csv data in localhost.

