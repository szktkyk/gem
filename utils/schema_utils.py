# PMIDのフィルターをどうするか
# genesymbolとかPMIDとかはリンクをつけたい
# pubdateもフィルタリングできると嬉しい
FILTER_TYPE_DICT = {
    "getool": "agSetColumnFilter",
    "pmid": "agTextColumnFilter",
    "pubtitle": "agTextColumnFilter",
    "pubdate": "agTextColumnFilter",
    "organism_name": "agSetColumnFilter",
    "taxonomy_category": "agSetColumnFilter",
    "genesymbol": "agTextColumnFilter",
    "biopro_id": "agSetColumnFilter",
    "RNA_seq": "agSetColumnFilter",
    "cellline_tissue": "agSetColumnFilter",
    "mutation_type": "agSetColumnFilter",
    "disease": "agSetColumnFilter",
}


VISIBLE_COLUMNS = [
    "getool",
    "pmid",
    "pubtitle",
    "pubdate",
    "organism_name",
    "taxonomy_category",
    "genesymbol",
    "biopro_id",
    "RNA_seq",
    "cellline_tissue",
    "mutation_type",
    "disease"
]

# RENDERER_TYPE_DICT = {
#     "getool": "Test",
#     "pmid":"",
#     "pubtitle": "",
#     "pubdate": "",
#     "organism_name": "",
#     "taxonomy_category": "",
#     "genesymbol": "",
#     "biopro_id": "",
#     "RNA_seq": "",
#     "cellline_tissue": "",
#     "Mutation_type": "",
#     "disease": "",
# }
