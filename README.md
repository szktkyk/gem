# GEM: Genome Editing Meta-database ver1
GEM is the subset of genome editing related metadata from PubMed articles. Extraction of metadata is achieved by utilizing the following databases. 
- PubMed
- PubMed Central
- NCBI gene
- PubTator Central
- MeSH
- NCBI taxonomy

## Usage
1. Run the scripts from W01 to W07 in modules directory.
2. `python app2.py` to build a local server to start a web application. (conda environment is written in `requirement.txt`)

## if you want to make your own dataset
Change searching terms in pubmed_terms in W01_Pubdetails.py.
