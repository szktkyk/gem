import re
import datetime

old_pubdetails = "./data/publication_details/20240504_pmidlist.txt"
search_query = '("crispr tech*"[All Fields] OR "gene edit*"[All Fields] OR "genome edit*"[All Fields] OR "genome writ*"[All Fields] OR "crispr cas*"[All Fields] OR "CRISPR-Associated Proteins"[MeSH Terms] OR  "CRISPR-Associated Protein 9"[MeSH Terms] OR "guide rna*"[All Fields] OR "sgrna"[All Fields] OR "sgrnas"[All Fields] OR "single guide rna*"[All Fields] OR “epigenome editing”[All Fields] OR ("cas9*"[All Fields] OR "cas12*"[All Fields] OR "cas3*"[All Fields] OR "sacas9*"[All Fields] OR "cas13*"[All Fields] OR "caslambda*"[All Fields] OR "cas7*"[All Fields] OR "casx*"[All Fields]) OR ("Transcription Activator-Like Effector Nucleases"[All Fields] OR "tal effector*"[All Fields] OR ("Transcription Activator-Like Effector Nucleases"[MeSH Terms] OR ("transcription"[All Fields] AND "activator like"[All Fields] AND "effector"[All Fields] AND "nucleases"[All Fields]) OR "talen"[All Fields] OR "talens"[All Fields])) OR ("zinc finger nuclease*"[All Fields] OR "zinc finger nucleases"[MeSH Terms] OR "ZFN"[All Fields]) OR ("Prime editing"[All Fields] OR "prime edit*"[All Fields] OR "Base editing"[All Fields] OR "base edit*"[All Fields] OR "crispr inter*"[All Fields] OR "crispr acti*"[All Fields] OR "target aid*"[All Fields] OR "crispr screen*"[All Fields] OR "crispr cas9 screen*"[All Fields] OR "crispr cas9 knockout screen*"[All Fields] OR "crispr dcas*"[All Fields] OR "crispr associated transposase*"[All Fields] OR "pitch system*"[All Fields] OR "precise integration into target chromosome*"[All Fields] OR "ddcbe*"[All Fields])) NOT "Review"[Publication Type]'

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")

updated_date = "2024-06-07"


PATH = {
    "pubdetails":"./data/publication_details/20240607_pubdetails.csv",
    "gene_annotation":"./data/csv_gitignore/20240607_gene_annotations.csv",
    "disease_annotation":"./data/csv_gitignore/20240607_disease_annotations.csv",
    "tissue_annotation":"./data/csv_gitignore/20240607_tissue_annotations.csv",
    "othermetadata":"./data/csv_gitignore/20240607_othermetadata.csv",
    "metadata":"./data/csv_gitignore/20240607_ge_metadata_all.json",
    "metadata_csv": "./data/csv_gitignore/20240607_ge_metadata.csv"
}


# referenced by the 8th annual meeting of the japanese society for genome editing abstract book.
parse_patterns = {
    "CRISPR-Cas9": re.compile("CRISPR.Cas9|\scas9|spcas9", re.IGNORECASE),
    "TALEN": re.compile(
        "TALEN|transciption.activator.like.effector.nuclease", re.IGNORECASE
    ),
    "ZFN": re.compile("ZFN|zinc.finger.nuclease", re.IGNORECASE),
    "Base editor": re.compile("Base.edit", re.IGNORECASE),
    "Prime editor": re.compile("Prime.Edit", re.IGNORECASE),
    "CRISPR-Cas3": re.compile("CRISPR.Cas3|cas3", re.IGNORECASE),
    "CRISPR-Cas12": re.compile("CRISPR.Cas12|cas12", re.IGNORECASE),
    "CRISPR-Cas13": re.compile("CRISPR.Cas13|cas13", re.IGNORECASE),
    "Casλ": re.compile("Casλ", re.IGNORECASE),
    "SaCas9": re.compile("SaCas9|KKH.SaCas9", re.IGNORECASE),
    # genome editing methods for below:
    "CRISPRi": re.compile("CRISPRi|CRISPR.interference"),
    "CRISPRa": re.compile("CRISPRa|CRISPR.activation"),
    "PITCh": re.compile("PITCh|PITCh.system|PITCh.method"),
    "TiD": re.compile("TiD|D.CRISPR.Cas.system"),
    "Target-AID": re.compile("Target-AID"),
    "CAST": re.compile("CRISPR.associated.transposase", re.IGNORECASE),
    "LoAD": re.compile("LoAD|local Accumulation of DSB repair molecules"),
    "CRISPR screen":re.compile("CRISPR.screen|CRISPR.cas9.screen|CRISPR.cas9.knockout.screen", re.IGNORECASE),
    "CRISPR CasX": re.compile("CRISPR.casx|\scasx", re.IGNORECASE),
    # others
    # "others": re.compile("CRISPR.Cas|crispr.technology|sgrna|gene.edit|genome.edit|gene.write|cas7|CRISPR.dcas", re.IGNORECASE),
}

