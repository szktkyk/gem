# Delete original gene2pubmed
# rm ../csv_gitignore/gene2pubmed.tsv

# Restore the updated gene2pubmed to the original format
awk -F "," '{print $2,$3,$4}' ../csv_gitignore/20221214_g2p_updated.csv | tr " " "\t" > ../csv_gitignore/`date "+%Y%m%d"`_g2p_updated_pre.tsv

# Delete duplicate lines
sort ../csv_gitignore/`date "+%Y%m%d"`_g2p_updated_pre.tsv| uniq  > ../csv_gitignore/`date "+%Y%m%d"`_g2p_updated.tsv

# Delete intermediate file
rm ../csv_gitignore/`date "+%Y%m%d"`_g2p_updated_pre.tsv

