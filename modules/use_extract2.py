import requests

def use_extract2(id_for_extract:str, df):
    # print(f"pmid in use_extract function: {id_for_extract}")
    input = ""
    df_row = df.filter(df["pmid"] == id_for_extract)
    input += str(df_row["title"][0])
    input += str(df_row["abstract"][0])

    extract_url = f"http://tagger.jensenlab.org/GetEntities?document={input}&entity_types=9606+-2+-25+-26+-27&format=tsv"
    # extract_url = f"http://tagger.jensenlab.org/GetEntities?document={input}&format=tsv"
    # print(extract_url)
    try:
        req = requests.get(extract_url)
        req.raise_for_status()
    except:
        print("error at extract2.0 API.")
        return [], [], [],[],[]

    extracted = req.text
    content = extracted.split("\n")
    if content == [''] or content[0].startswith("<?xml"):
        print("no results in extract2.0.")
        return [], [], [], [],[]
    print(f"extracted_words:{content}")
    # 出力されるtsvの真ん中の列の数字によってその単語が何に分類されるかを判断する
    # -2だと生物種
    # マイナスがついていなければ遺伝子名
    # -25だと組織名
    # -26だと疾患名
    disease = []
    tissue = []
    species = []
    genes_human = []
    genes_other = []
    not_focus = ['-27','-21','-22','-23','-1']
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
            genes_human.append(l[2])
            continue
        if l[1] in not_focus:
            continue

        else:
            genes_other.append({"gene":l[0],"species":l[1]})

    species = list(set(species))
    genes_human = list(set(genes_human))
    # genes_other = list(set(genes_other))   

    return genes_human, genes_other, species, disease, tissue

  