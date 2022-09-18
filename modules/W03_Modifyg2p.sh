# Delete original gene2pubmed
rm ../data/gene2pubmed

# Restore the updated gene2pubmed to the original format
awk -F "," '{print $2,$3,$4}' ../data/`date "+%Y%m%d"`/`date "+%Y%m%d"`_g2p_updated.csv | tr " " "\t" > ../data/`date "+%Y%m%d"`/`date "+%Y%m%d"`_g2p_updated_pre.tsv

# Delete duplicate lines
sort ../data/`date "+%Y%m%d"`/`date "+%Y%m%d"`_g2p_updated_pre.tsv| uniq  > ../data/`date "+%Y%m%d"`/`date "+%Y%m%d"`_g2p_updated.tsv

# Delete intermediate file
rm ../data/`date "+%Y%m%d"`/`date "+%Y%m%d"`_g2p_updated_pre.tsv

