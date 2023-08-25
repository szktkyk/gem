## Genome Editing Meta-database (GEM)
- It is a dataset of genome editing related metadata automatically extracted from PubMed articles. Extraction of metadata is achieved by utilizing the following databases and systems.
    - PubMed
    - PubMed Central
    - NCBI gene
    - PubTator
    - MeSH
    - NCBI taxonomy
    - EXTRACT 2.0 (https://extract.jensenlab.org/)

- `{date}_ge_metadata.csv` is the outcome dataset.
- We prepare the web interface (https://bonohu.hiroshima-u.ac.jp/gem) for users to search and retrieve metadata.

## Update 2023/8/22
- We started using [EXTRACT 2.0](https://extract.jensenlab.org/)(doi: 10.1101/111088) for articles from which we could not extract metadata with NCBI related databases. 
- 42,414 literatures with 86,348 metadata entries with 2,701 species are archived.

## Used data for metadata collection
- gene_info.gz (https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz) (downloaded at 2023-Aug-16)
- mtrees2023.bin (https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/meshtrees/mtrees2023.bin) (downloaded at 2023-Aug-16)
- new_taxdump (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) (downloaded at 2022-Dec-12)

## Publication
- (Peer-reviewed short communication) GEM: Genome Editing Meta-database, a dataset of genome editing related metadata systematically extracted from PubMed literatures.
Gene and Genome Editing 22Dec2022, doi: 10.1016/j.ggedit.2022.100024