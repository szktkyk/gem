# About 2 DAYS for 47000 articles
import config
import polars as pl
from modules import eutils, use_extract2, ncbi_datasets as nd, pubtator, match, read_log, check_results
import ast
import sqlite3
import csv

con = sqlite3.connect("./data/gem.db")

def main():
    df = pl.read_csv(config.PATH["pubdetails"])
    pmids_list = df["pmid"].to_list()
    print(f"The number of pmids: {len(pmids_list)}")
    # pmids_list = check_results.get_pmids_from_geneann()
    # print(f"The number of pmids from geneann: {len(pmids_list)}")
    
    list_of_chunked_pmids = eutils.generate_chunked_id_list(pmids_list, 100)
    extracted_genes = []
    extracted_disease = []
    extracted_tissue = []
    for a_chunked_pmids in list_of_chunked_pmids:
        results = get_annotation(a_chunked_pmids, df)
        extracted_genes.extend(results["extracted_genes"])
        extracted_disease.extend(results["extracted_disease"])
        extracted_tissue.extend(results["extracted_tissue"])

    field_name_gene = ["pmid","species","gene",]
    field_name_disease = ["pmid","disease",]
    field_name_tissue = ["pmid","tissue",]
    with open(
        f"./data/csv_gitignore/{config.date}_gene_annotations.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_gene)
        writer.writeheader()
        writer.writerows(extracted_genes)

    with open(
        f"./data/csv_gitignore/{config.date}_disease_annotations.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_disease)
        writer.writeheader()
        writer.writerows(extracted_disease)

    with open(
        f"./data/csv_gitignore/{config.date}_tissue_annotations.csv",
        "w",
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name_tissue)
        writer.writeheader()
        writer.writerows(extracted_tissue)



def get_annotation(a_chunked_pmids, df):
    extracted_genes = []
    extracted_disease = []
    extracted_tissue = []
    a_chunked_pmids = [str(i) for i in a_chunked_pmids]
    pmids_str = ",".join(a_chunked_pmids)
    # if add "full-texts" at the end of the url, you can get the full-texts of the articles.
    # but this time, only title and abstract are used. so it's not necessary.
    pt_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocxml?pmids={pmids_str}"
    print(f"\nnew pt_url:{pt_url}")
    try:
        tree_pubtator = eutils.use_eutils(pt_url)
    except:
        print(f"Pubtator api error at {pt_url}.")
        pass
    # categorize the pmids into two groups: one for extract2.0 and the other for pubtator
    pt_pmids = []
    for element in tree_pubtator.findall("./document"):
        tmp_pmid = element.find("id").text
        pt_pmids.append(tmp_pmid)
    go_to_extract = list(set(a_chunked_pmids) - set(pt_pmids))
    print(f"pmids for extract2 : {len(go_to_extract)}")
    print(f"pmids for pubtator : {len(pt_pmids)}")

    # all pmids processing for substances and mesh
    for pmid in a_chunked_pmids:
        print(f"\npmid:{pmid}....")
        # temporary lists for each pmid
        tmp_species = []
        tmp_genes = []
        tmp2 = []

        df_row = df.filter(df["pmid"] == pmid)
        substances = df_row["substances"][0]
        mesh = df_row["mesh"][0]          
        substances = ast.literal_eval(substances)
        mesh_list = ast.literal_eval(mesh)

        # 1. Check Substances
        substances_genes = [s for s in substances if "protein," in s]
        if substances_genes != []:
            print(f"substances_genes{substances_genes}")
            for a_substance in substances_genes:
                splited = a_substance.split(",")
                taxname = splited[1].lstrip()
                protein = splited[0]

                try:
                    cur = con.execute(f"select tax_id from taxonomy where tax_name like '{taxname}'",)
                    rs = cur.fetchone()
                    if rs == None:
                        print(f"No taxid for {taxname} from substances. Go to next substances.")
                        continue
                    else:
                        taxid = rs[0]
                        # print(taxid)  
                    gene = protein.split()[0]
                    geneid = nd.get_geneid_from_genesymbol(gene,taxid)          
                    extracted_genes.append({"pmid":pmid,"species": taxid, "gene": geneid})
                    tmp2.append({"pmid":pmid,"species": taxid, "gene": geneid})
                    print({"pmid":pmid,"species": taxid, "gene": geneid})
                except:
                    print(f"error at obtaining taxid from substances. Go to next substances.")

        else:
            print("no substances_genes. Go to the MeSH part..")
            pass

        # 2. Check MeSH
        if mesh_list != []:
            for a_mesh in mesh_list:
                cur = con.execute(f"select mesh_number from mtree where mesh_term = ?", (a_mesh,))
                rs = cur.fetchone()
                if rs == None:
                    print(f"error at obtaining mesh_number for {a_mesh} from MESH. next loop")
                    continue
                else:
                    treeid = rs[0]

                if treeid.startswith("B") and len(treeid.split('.')) > 5:
                    try:
                        cur = con.execute(f"select tax_id from taxonomy where tax_name like '{a_mesh}'")
                        rs = cur.fetchone()
                        if rs == None:
                            print(f"error at obtaining taxid for {a_mesh} from MeSH. Go to next MeSH term.")
                            continue
                        else:
                            taxid = rs[0]
                        if taxid != None:
                            tmp_species.append(taxid)
                        else:
                            pass
                    except:
                        print(f"error at obtaining taxid from MeSH. Go to next MeSH term")
                        continue
            print(f"species from mesh_part: {tmp_species}")
        else:
            print("no species from the mesh found for this pmid. keep the loop going.")
            pass

        # 3. EXTRACT2.0
        if pmid in go_to_extract:
            print(f"pmid:{pmid} working on EXTRACT2.0...")
            genes_human, genes_other, species_ext, disease_ext, tissue_ext = use_extract2.use_extract2(pmid,df)

            for g_h in genes_human:
                ncbigene_human = nd.ensg2ncbi(g_h)
                extracted_genes.append({"pmid":pmid,"species": "9606", "gene": ncbigene_human})
                tmp2.append({"pmid":pmid,"species": "9606", "gene": ncbigene_human})
                print({"pmid":pmid,"species": "9606", "gene": ncbigene_human})

            for d in genes_other:
                d_gene = d["gene"]
                d_species = d["species"]
                geneid_oth = nd.get_geneid_from_genesymbol(d_gene,d_species)
                extracted_genes.append({"pmid":pmid,"species": d_species, "gene": geneid_oth})
                tmp2.append({"pmid":pmid,"species": d_species, "gene": geneid_oth})
                print({"pmid":pmid,"species": d_species, "gene": geneid_oth})
            
            tmp_species.extend(species_ext)
            if disease_ext != []:
                extracted_disease.append({"disease":disease_ext,"pmid":pmid})
                print({"disease":disease_ext,"pmid":pmid})
            if tissue_ext != []:
                extracted_tissue.append({"tissue":tissue_ext,"pmid":pmid})
                print({"tissue":tissue_ext,"pmid":pmid})         
        
        # 4. PubTator
        elif pmid in pt_pmids:
            print(f"pmid:{pmid} working on PubTator...")
            element = tree_pubtator.find(f"./document[id='{pmid}']")
            # 4-1. Check Species from TITLE
            annotations_title = pubtator.get_annotation_from_section(element, "title")
            if annotations_title != None:
                for a in annotations_title:
                    if a.find("infon[@key='type']").text == "Species" and a.find("infon[@key='identifier']") != None:
                        pt_taxid_title = a.find("infon[@key='identifier']").text
                        if ";" in pt_taxid_title:
                            pt_taxid_title = pt_taxid_title.split(";")[0]
                            tmp_species.append(pt_taxid_title)
                        else:
                            tmp_species.append(pt_taxid_title)
                    elif a.find("infon[@key='type']").text == "Species" and a.find("infon[@key='identifier']") == None:
                        pt_taxname = a.find("text").text
                        try:
                            cur = con.execute(f"select tax_id from taxonomy where tax_name like '{pt_taxname}'")
                            rs = cur.fetchone()
                            if rs == None:
                                print(f"error at obtaining taxid for {pt_taxname} from pubtator..")
                                continue
                            else:
                                pt_taxid = rs[0]
                            if pt_taxid != None:
                                tmp_species.append(pt_taxid)
                        except:
                            print(f"error at obtaining taxid for {pt_taxname} from pubtator..")
                            continue
                    else:
                        continue

            else:
                pass
            
            # 4-2. Check Species from ABSTRACT (if tmp_species = [])
            if tmp_species == []:
                annotations_abstract = pubtator.get_annotation_from_section(element, "abstract")
                for b in annotations_abstract:
                    if b.find("infon[@key='type']").text == "Species" and b.find("infon[@key='identifier']") != None:
                        pt_taxid_abst = b.find("infon[@key='identifier']").text
                        if ";" in pt_taxid_abst:
                            pt_taxid_abst = pt_taxid_abst.split(";")[0]
                            tmp_species.append(pt_taxid_abst)
                        else:
                            tmp_species.append(pt_taxid_abst)
                    elif b.find("infon[@key='type']").text == "Species" and b.find("infon[@key='identifier']") == None:
                        pt_taxname = b.find("text").text
                        try:
                            cur = con.execute(f"select tax_id from taxonomy where tax_name like '{pt_taxname}'")
                            rs = cur.fetchone()
                            if rs == None:
                                print(f"error at obtaining taxid for {pt_taxname} from pubtator..")
                                continue
                            else:
                                pt_taxid = rs[0]
                            if pt_taxid != None:
                                tmp_species.append(pt_taxid)
                        except:
                            print(f"error at obtaining taxid for {pt_taxname} from pubtator..")
                            continue
                    else:
                        continue
            else:
                pass
            
            # 4-3. Check Genes, Diseases, Celltypes
            tmp_genes_pt, disease, cellline = pubtator.get_annotation_ptc(element)
            tmp_genes.extend(tmp_genes_pt)
            if disease != []:
                extracted_disease.append({"disease":disease,"pmid":pmid})
                print({"disease":disease,"pmid":pmid})  

            if cellline != []:
                extracted_tissue.append({"tissue":cellline,"pmid":pmid})
                print({"tissue":cellline,"pmid":pmid})
            

        # 5-1. Gene and Species MATCHING
        tmp_genes = list(set(tmp_genes)) 
        tmp_genes = [x for x in tmp_genes if x != "NotFound"]   
        print(f"tmp_genes:{tmp_genes}")
        print(f"tmp_species:{tmp_species}")
        mt_genes, mt_species = match.match_genes_species(tmp_genes,tmp_species,pmid)
        extracted_genes.extend(mt_genes)
        tmp2.extend(mt_genes)       

        # 5-2. If no match at all, add species to metadata
        if len(tmp2) < 2 and mt_species != []:
            extracted_genes.append({"pmid":pmid,"species": mt_species[0], "gene": "NotFound"})
            print({"pmid":pmid,"species": mt_species[0], "gene": "NotFound"})     
        if tmp2 == [] and mt_species != []:
            try:
                extracted_genes.append({"pmid":pmid,"species": mt_species[1], "gene": "NotFound"})
                print({"pmid":pmid,"species": mt_species[1], "gene": "NotFound"})
            except:
                print("Only one taxonomy obtained in the tmp_species. next loop..")
                continue          
        else:
            continue
        
    results = {"extracted_genes":extracted_genes,"extracted_disease":extracted_disease,"extracted_tissue":extracted_tissue}

    return results


if __name__ == "__main__":
    main()