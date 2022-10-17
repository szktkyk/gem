# GEM: Genome Editing Meta-database ver1
## What is GEM?
- GEM is the dataset of genome editing related metadata from PubMed articles. Extraction of metadata is achieved by utilizing the following databases. 
    - PubMed
    - PubMed Central
    - NCBI gene
    - PubTator Central
    - MeSH
    - NCBI taxonomy

## Usage
1. install miniconda
2. move to the gem directory
3. `conda create -n gemenv --file env_name_intel.txt`
4. `conda activate gemenv`
5. `python app.py` to start the web application in your localhost.

## if you want to make your own dataset
1. Write searching terms in pubmed_terms in W01_Pubdetails.py.
2. Build DB by executing from `DB1_Geneinfo.py` to `DB4_Taxonomy.py`
3. `python W01_Pubdetails.py`
4. Insert pubdetails into DB by executing `DB7_Pubdetails.py`
5. `python W02_Update_Gene2pubmed.py`
6. `sh W03_Modifyg2p.sh`
7. Insert updated gene2pubmed into DB by executing `DB6_Metadata.py`
8. `python W05_CreateMetadata.py` to get the json file containing metadata.
9. Insert metadata into DB by executing `W05_MetadataIntoDB.py`
10. Write a path to json file in app.py.
11. `python app.py` to see the json data in localhost.