import sqlite3
import pandas as pd
import ast
import collections
import config
import csv
import time
import requests
from modules import pubtator, use_extract2, eutils


DATABASE = "data/gem.db"
con = sqlite3.connect(DATABASE)



def main():
    """
    use e-utilities to get publication details and to make a csv file
    """
    pmids = con.execute("select pmid from tmp_pubdetails")
    pmids = pmids.fetchall()
    pmids_list = []
    for x in pmids:
        pmids_list.append(x[0])
    print(f"The number of pmids: {len(pmids_list)}")
    # pmids_list = ["34425703"]
    extracted_genes, extracted_disease, extracted_tissue = get_annotation(pmids_list)
    field_name_gene = [
        "pmid",
        "species",
        "gene",
    ]
    field_name_disease = [
        "pmid",
        "disease",
    ]
    field_name_tissue = [
        "pmid",
        "tissue",
    ]
    with open(
        f"./csv_gitignore/{config.date}_gene_annotations.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_gene)
        writer.writeheader()
        writer.writerows(extracted_genes)

    with open(
        f"./csv_gitignore/{config.date}_disease_annotations.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_disease)
        writer.writeheader()
        writer.writerows(extracted_disease)

    with open(
        f"./csv_gitignore/{config.date}_tissue_annotations.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_tissue)
        writer.writeheader()
        writer.writerows(extracted_tissue)


def get_annotation(pmids):
    # 最後に出力するリスト2つを定義
    extracted_genes = []
    extracted_disease = []
    extracted_tissue = []
    list_of_chunked_pmids = eutils.generate_chunked_id_list(pmids, 100)
    # print(list_of_chunked_pmids)
    for a_chunked_pmids in list_of_chunked_pmids:
        pmids_str = ",".join(a_chunked_pmids)
        pt_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids={pmids_str}"
        print(f"\nnew pt_url:{pt_url}")
        try:
            tree_pubtator = eutils.use_eutils(pt_url)
        except:
            print(f"Pubtator api error at {pt_url}. loop continue.")
            pass
        
        # pubtatorで取得できなかったIDを抽出. あとでextract2で処理する。
        pt_pmids = []
        for element in tree_pubtator.findall("./document"):
            tmp_pmid = element.find("id").text
            pt_pmids.append(tmp_pmid)
        go_to_extract = list(set(a_chunked_pmids) - set(pt_pmids))
        print(f"pmids for extract2 (ids that not found in PubTator): {go_to_extract}")

        # pubtatorで取得できたIDを処理
        for pmid in pt_pmids:
            print(f"\npmid:{pmid}....")
            tmp_species = []
            tmp_genes = []
            tmp2 = []
            substances_cur = con.execute(f"select substances from tmp_pubdetails where pmid = '{pmid}'")
            substances = substances_cur.fetchone()[0]
            mesh_cur = con.execute(f"select mesh from tmp_pubdetails where pmid = '{pmid}'")
            mesh = mesh_cur.fetchone()[0]
            
            substances = ast.literal_eval(substances)
            mesh_list = ast.literal_eval(mesh)

            # 1. check substances
            substances_genes = [s for s in substances if "protein," in s]
            if substances_genes != []:
                print(f"substances_genes{substances_genes}")
                for a_substance in substances_genes:
                    splited = a_substance.split(",")
                    taxname = splited[1].lstrip()
                    protein = splited[0]
                    try:
                        cur = con.execute(f"select tax_id from taxonomy where tax_name like '{taxname}'")
                        rs = cur.fetchone()
                        if rs == None:
                            print(f"error at obtaining taxid for {taxname} from substances. next loop.")
                            continue
                        else:
                            taxid = rs[0]
                        gene = protein.split()[0]
                        #TODO: gene_infoの"Synonyms"列に遺伝子名が入ってるケースがある??ので対応させる
                        cur2 = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(taxid,gene))
                        rs2 = cur2.fetchone()
                        if rs2 == None:
                            print(f"error at obtaining substance_gene for {gene}. next loop.")
                            continue
                        else:
                            geneid = rs2[0]
                    except:
                        print(f"syntax error at substances. next loop")
                        continue
                    extracted_genes.append({"pmid":pmid,"species": taxid, "gene": geneid})
                    tmp2.append({"pmid":pmid,"species": taxid, "gene": geneid})
                    print({"pmid":pmid,"species": taxid, "gene": geneid})
            else:
                print("no substances genes found for this pmid. keep the loop going.")
                pass

            # 2. check mesh for candidate species
            if mesh_list != []:
                for a_mesh in mesh_list:
                    try:
                        cur = con.execute(f"select mesh_number from mtree where mesh_term = '{a_mesh}'")
                        rs = cur.fetchone()
                        if rs == None:
                            print(f"error at obtaining mesh_number for {a_mesh} from MESH. next loop")
                            continue
                        else:
                            treeid = rs[0]

                        if treeid.startswith("B") and len(treeid.split('.')) > 5:
                            cur2 = con.execute(f"select tax_id from taxonomy where tax_name like '{a_mesh}'")
                            rs2 = cur2.fetchone()
                            if rs2 == None:
                                print(f"error at obtaining taxid for {a_mesh} from MeSH_tree_ID. next loop")
                                continue
                            else:
                                taxid = rs2[0]
                                tmp_species.append(taxid)
                    except:
                        print(f"syntax error at mesh. loop continue. next loop")
                        continue
                print(f"species from mesh_part: {tmp_species}")
            else:
                print("no species from the mesh found for this pmid. keep the loop going.")
                pass
            
            # 3. check pubtator
            element = tree_pubtator.find(f"./document[id='{pmid}']")
            # 3-1. check candidate species from title section
            annotations_title = pubtator.get_annotation_from_section(element, "title")
            if annotations_title != None:
                for a in annotations_title:
                    if a.find("infon[@key='type']").text == "Species":
                        try:
                            tmp_species.append(a.find("infon[@key='identifier']").text)
                        except:
                            continue
                    else:
                        continue
            else:
                pass
            
            # 3-1-2. check candidate species from abstract section if species not found from mesh and title
            if tmp_species == []:
                annotations_abstract = pubtator.get_annotation_from_section(element, "abstract")
                for b in annotations_abstract:
                    if b.find("infon[@key='type']").text == "Species":
                        try:
                            tmp_species.append(b.find("infon[@key='identifier']").text)
                        except:
                            continue
            else:
                pass

            # pubtatorでタイトルとアブスト全部のアノテーションを取得
            tmp_genes, disease = pubtator.get_annotation_ptc(element)

            # 3-2. append extracted diseases to the list
            disease = list(set(disease))
            disease_str = ",".join(disease)
            extracted_disease.append({"disease":disease_str,"pmid":pmid})
            print({"disease":disease_str,"pmid":pmid})      

            # 3-3. 遺伝子と生物種について処理
            tmp_genes = list(set(tmp_genes))          
            print(f"tmp_genes (added genes from pubtator):{tmp_genes}")
            print(f"tmp_species (added species from pubtator):{tmp_species}")

            # 生物種はカウント順に並べ替える
            species_counts = collections.Counter(tmp_species).most_common(20)
            print(f"species_count:{species_counts}")
            tmp_species = []
            for species_count in species_counts:
                tmp_species.append(species_count[0])
            print(f"tmp_species (arranged in order of count):{tmp_species}")

            # 遺伝子と生物種のマッチング
            for a_gene in tmp_genes:
                try:
                    cur = con.execute(f"select tax_id from gene_info where GeneID = '{a_gene}'")
                except:
                    print(f"syntax error at {a_gene}. next loop..")
                    continue
                try:
                    rs = cur.fetchone()
                    if rs[0] in tmp_species:
                        extracted_genes.append({"pmid":pmid,"species": rs[0], "gene": a_gene})
                        tmp2.append({"pmid":pmid,"species": rs[0], "gene": a_gene})
                        print({"pmid":pmid,"species": rs[0], "gene": a_gene})
                    else:
                        # print("no pair for {} and {}. next loop".format(rs[0],a_gene))
                        continue
                except:
                    print(f"something wrong with rs for {a_gene}. next loop")
                    continue

            # もし何もマッチしない場合は生物種のみエントリーに含める
            if tmp2 == [] and tmp_species != []:
                extracted_genes.append({"pmid":pmid,"species": tmp_species[0], "gene": "NotFound"})
                tmp2.append({"pmid":pmid,"species": tmp_species[0], "gene": "NotFound"})
                print({"pmid":pmid,"species": tmp_species[0], "gene": "NotFound"})
                try:
                    extracted_genes.append({"pmid":pmid,"species": tmp_species[1], "gene": "NotFound"})
                    tmp2.append({"pmid":pmid,"species": tmp_species[1], "gene": "NotFound"})
                    print({"pmid":pmid,"species": tmp_species[1], "gene": "NotFound"})
                except:
                    print("Only one taxonomy obtained in the tmp_species. next loop..")
                    continue     
            
            if tmp2 != []:
                print("tmp2 is not empty. next loop..")
                continue
            # エントリーが何もなければ後ほどEXTRACT2.0で処理する
            else:
                go_to_extract.append(pmid)
                print("no species or genes found for this pmid. PMID added for EXTRACT2.0. next loop..")  
                continue

     
        # # 4. use EXTRACT2.0 to extract genes and diseases if no genes were extracted from pubtator
        # 処理が必要なPMIDについてEXTRACT2.0で処理する
        if go_to_extract != []:
            print("some of pmids have no annotations. use EXTRACT2.0")
            print(f"go_to_extract:{go_to_extract}")
            for pmid in go_to_extract:
                print(f"\npmid:{pmid}....")
                metadata, disease, tissue = use_extract2.use_extract2(pmid,con)
                if metadata == []:
                    print("no gene and species found in EXTRACT2.0 for this pmid. loop pass...")
                    pass
                else:
                    for a_metadata in metadata:
                        extracted_genes.append(a_metadata)
                        print(a_metadata)
                if disease == []:
                    print("no disease found in EXTRACT2.0 for this pmid. loop pass...")
                    pass
                else:
                    disease = list(set(disease))
                    disease_str = ",".join(disease)
                    extracted_disease.append({"disease":disease_str,"pmid":pmid})
                    print({"disease":disease_str,"pmid":pmid})
                if tissue == []:
                    print("no tissue found in EXTRACT2.0 for this pmid. loop pass...")
                    pass
                else:
                    tissue = list(set(tissue))
                    tissue_str = ",".join(tissue)
                    extracted_tissue.append({"tissue":tissue_str,"pmid":pmid})
                    print({"tissue":tissue_str,"pmid":pmid})
                
        else:
            continue

    return extracted_genes, extracted_disease, extracted_tissue



if __name__ == "__main__":
    main()