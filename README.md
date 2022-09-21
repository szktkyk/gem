# GEM: Genome Editing Meta-database ver1
## What is GEM?
- GEM is the subset of genome editing related metadata from PubMed articles. Extraction of metadata is achieved by utilizing the following databases. 
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
2. `python W01_Pubdetails.py`
3. `python W02_Update_Gene2pubmed.py`
4. `sh W03_Modifyg2p.sh`
5. `python W04_GeneCounts.py`
6. `python W05_CreateMetadata.py` to get the Json file containing metadata.
7. Write a path to json file in app.py.
8. `python app.py` to see the json data in localhost.