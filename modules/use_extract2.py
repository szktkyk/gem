import requests
import sys


def use_extract2(id_for_extract:str, con):
    print(f"pmid in use_extract function: {id_for_extract}")
    for_join = []
    title_cur = con.execute(f"select title from tmp_pubdetails where pmid = '{id_for_extract}'")
    for_join.append(title_cur.fetchone()[0])
    abstract_cur = con.execute(f"select abstract from tmp_pubdetails where pmid = '{id_for_extract}'")
    for_join.append(abstract_cur.fetchone()[0])
    input = ",".join(for_join)

    extract_url = f"http://tagger.jensenlab.org/GetEntities?document={input}&entity_types=9606+-2+-25+-26+-27&format=tsv"
    
    # extract_url = f"http://tagger.jensenlab.org/GetEntities?document={input}&format=tsv"
    print(extract_url)
    try:
        req = requests.get(extract_url)
        req.raise_for_status()
    except:
        print("error at extract2.0 API.")
        return [], [], []

    extracted = req.text
    content = extracted.split("\n")
    if content == [''] or content[0].startswith("<?xml"):
        print("no results in extract2.0.")
        return [], [], []
    print(f"extracted_words:{content}")
    # 出力されるtsvの真ん中の列の数字によってその単語が何に分類されるかを判断する
    # -2だと生物種
    # マイナスがついていなければ遺伝子名
    # -25だと組織名
    # -26だと疾患名
    disease = []
    tissue = []
    species = []
    genes = []
    metadata = []
    for item in content:
        l = item.split("\t")
        if l[1] == '-26':
            disease.append(l[0])
            continue
        if l[1] == '-25':
            tissue.append(l[0])
            continue
        if l[1] == '-2':
            species.append(l[2])
            continue
        if l[1] == '9606':
            genes.append(l[0])
            species.append(l[1])
            continue
        if l[1] == '-27':
            print(f"-27:{l}")
            continue
        else:
            try:
                genes.append(l[0])
            except:
                print(f"no results in extract2.0. next loop.{l}")
                continue
    species = list(set(species))
    genes = list(set(genes))

    for a_species in species:
        for a_gene in genes:
            try:
                cur = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(a_species,a_gene))
            except:
                print(f"syntax error at {a_gene}. Keep the loop going. next loop.")
                geneid = "NotFound"
                continue
            rs = cur.fetchone()
            if rs == None:
                # print("no pair for {} and {}".format(a_species,a_gene))
                continue
            else:
                geneid = rs[0]
            metadata.append({"pmid":id_for_extract, "species":a_species, "gene":geneid,})

    if metadata == [] and genes == [] and species != []:
        for a_species in species:
            metadata.append({"pmid":id_for_extract, "species":a_species, "gene":"NotFound",})
    
    return metadata, disease, tissue
        # try:
        #     a_gene = l[0]
        #     a_species = l[1]
        # except:
        #     print("no results in extract2.0. next loop.")
        #     geneid = "NotFound"
        #     a_species = "NotFound"
        #     continue
        # try:
        #     cur = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(a_species,a_gene))
        # except:
        #     print(f"syntax error at {a_gene}. Keep the loop going. next loop.")
        #     geneid = "NotFound"
        #     continue
        # rs = cur.fetchone()
        # if rs == None:
        #     print("no pair for {} and {}".format(a_species,a_gene))
        #     geneid = "NotFound"
        #     a_species = "NotFound"
        #     continue
        # else:
        #     geneid = rs[0]
    # return geneid, a_species