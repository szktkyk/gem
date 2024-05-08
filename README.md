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

## Update 2024/5/8
- We have updated the metadata as duplicated or unnecessary entries have been deleted. 47,583 literatures with 86,615 metadata entries with 1,321 species are archived. 
- The web interface has been updated.
- We have started using [NCBI datasets cli](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/) instead of gene_info.gz. 

## Update 2023/8/22
- We started using [EXTRACT 2.0](https://extract.jensenlab.org/)(doi: 10.1101/111088) for articles from which we could not extract metadata with NCBI related databases. 
- 42,414 literatures with 86,348 metadata entries with 2,701 species are archived.

## Used data for metadata collection
~~- gene_info.gz (https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz) (downloaded at 2023-Aug-16)~~ 
- mtrees2023.bin (https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/meshtrees/mtrees2023.bin) (downloaded at 2023-Aug-16)
- taxidlineage.dmp (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) (downloaded at ~~2022-Dec-12~~ 2024-May-07)
- names.dmp (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/ downloaded at 2022-Dec-12. Manually repaired file (ex: set 9606 for "Homo sapiens" instead of "Homo sapiens Linnaeus"))

## Publication
- (Peer-reviewed short communication) GEM: Genome Editing Meta-database, a dataset of genome editing related metadata systematically extracted from PubMed literatures.
Gene and Genome Editing 22Dec2022, doi: 10.1016/j.ggedit.2022.100024

## To run GEM locally
- `pip install -r requirements.txt`
- Install NCBI Datasets command-line tools followed by [instructions](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/).
- Prepare `gem.db` in data repository (We have used the codes in the update_db repository).
- `python app.py`