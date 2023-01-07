import sqlite3
import pandas as pd
import ast
from ModulesForW02 import *
import collections
import datetime

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")

data_list =[]
# Amphibians or Birds or Fishes or Mammals or Reptiles or Plants or Insecta
species_category = []
DATABASE = "../data/gem.db"
con = sqlite3.connect(DATABASE)

# process pmids with pmcid available
pmid1 = con.execute("select pmid from pubdetails where pmcid != 'Not found'")
pmids_with_pmcid = pmid1.fetchall()

print("the total number of pmids with pmcid available :{}".format(len(pmids_with_pmcid)))

for x in pmids_with_pmcid:
    pmid = x[0]
    tmp_datalist = []
    species = []
    genes = []
    print(f"\npmid:{pmid}....")
    pmcid_cur = con.execute(f"select pmcid from pubdetails where pmid = '{pmid}'")
    pmcid = pmcid_cur.fetchone()[0]
    substances_cur = con.execute(f"select substances from pubdetails where pmid = '{pmid}'")
    substances = substances_cur.fetchone()[0]
    mesh_cur = con.execute(f"select mesh from pubdetails where pmid = '{pmid}'")
    mesh = mesh_cur.fetchone()[0]
    
    substances = ast.literal_eval(substances)
    mesh_list = ast.literal_eval(mesh)

    # 1. check substances for gene extraction
    substances_genes = [s for s in substances if "protein," in s]
    if substances_genes != []:
        print(f"substances_genes{substances_genes}")
        for a_substance in substances_genes:
            splited = a_substance.split(",")
            taxname = splited[1].lstrip()
            print(taxname)
            protein = splited[0]
            try:
                cur = con.execute(f"select tax_id from taxonomy where tax_name like '{taxname}'")
                rs = cur.fetchone()
                if rs == None:
                    print(f"error at substance_tax for {taxname}")
                    pass
                else:
                    taxid = rs[0]
                gene = protein.split()[0]
                cur2 = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(taxid,gene))
                rs2 = cur2.fetchone()
                if rs2 == None:
                    print(f"error at substance_gene for {gene}")
                    pass
                else:
                    geneid = rs2[0]
            except:
                print(f"syntax error at substances. loop continue")
                continue
            data_list.append({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})
            tmp_datalist.append({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})
            print(({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid}))


    # 2. check mesh for species extraction
    if mesh_list != []:
        try:
            for a_mesh in mesh_list:
                cur = con.execute(f"select mesh_number from mtree where mesh_term = '{a_mesh}'")
                rs = cur.fetchone()
                if rs == None:
                    print(f"error at obtaining mesh_number for {a_mesh}")
                    pass
                else:
                    treeid = rs[0]
                
                # ↓review required
                # # select if Amphibians
                # if treeid.startswith("B01.050.150.900.090"):
                #     species_category.append({"pmid": pmid, "species_category": "Amphibians"})
                #     print({"pmid": pmid, "species_category": "Amphibians"})
                # # select if Birds
                # if treeid.startswith("B01.050.150.900.248"):
                #     species_category.append({"pmid": pmid, "species_category": "Birds"})
                #     print({"pmid": pmid, "species_category": "Birds"})
                # # select if Fishes
                # if treeid.startswith("B01.050.150.900.493"):
                #     species_category.append({"pmid": pmid, "species_category": "Fishes"})
                #     print({"pmid": pmid, "species_category": "Fishes"})
                # # select if Mammals
                # if treeid.startswith("B01.050.150.900.649"):
                #     species_category.append({"pmid": pmid, "species_category": "Mammals"})
                #     print({"pmid": pmid, "species_category": "Mammals"})
                # # select if Reptiles
                # if treeid.startswith("B01.050.150.900.833"):
                #     species_category.append({"pmid": pmid, "species_category": "Reptiles"})
                #     print({"pmid": pmid, "species_category": "Reptiles"})
                # # select if Reptiles
                # if treeid.startswith("B01.050.500.131.617"):
                #     species_category.append({"pmid": pmid, "species_category": "Insecta"})
                #     print({"pmid": pmid, "species_category": "Insecta"})
                
                # Extract Species names
                if treeid.startswith("B") and len(treeid.split('.')) > 5:
                    cur2 = con.execute(f"select tax_id from taxonomy where tax_name like '{a_mesh}'")
                    rs2 = cur2.fetchone()
                    if rs2 == None:
                        print(f"error at obtaining taxid from mesh for {a_mesh}")
                        pass
                    else:
                        taxid = rs2[0]
                        species.append(taxid)
                        print(f"species_{taxid} is obtained from MESH")
        except:
            print("error around mesh scripts")

    # 3. Use PubTator Central if no information from MeSH
    if tmp_datalist != []:
        print("already obtained gene and species. Loop continue..")
        continue
    else:
        print("move to pubtator central process..")
        ptc_genes = []
        tmp2 = []
        ptc_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmcids={pmcid}"
        try:
            tree_ptc = use_eutils(ptc_url)
        except:
            print(f"pubtator api error at {ptc_url}")

        if not tree_ptc.find("./document"):
            print("No document in ptc.")
            pass

        else:
            try:
                genes, species_ptc = get_annotations_ptc(tree_ptc)
                genes_count = collections.Counter(genes).most_common(20)
                print(f"genes_count:{genes_count}")
                for gene_count in genes_count:
                    # Extraction of genes that have been text mined more than 5 times from RESULTS or ABSTRACT
                    if gene_count[1] > 15:
                        ptc_genes.append(gene_count[0])
                    else:
                        continue
                print(f"ptc_genes:{ptc_genes}")
                species_count = collections.Counter(species_ptc).most_common(20)
                print(f"species_count:{species_count}")
                for specie_count in species_count:
                    # Extraction of genes that have been text mined more than 10 times from METHODS or ABSTRACT
                    if specie_count[1] > 10:
                        taxname = specie_count[0]
                        # print(taxname)
                        cur = con.execute(f"select tax_id from taxonomy where tax_name like '{taxname}'")
                        rs = cur.fetchone()
                        if rs == None:
                            pass
                        else:
                            taxid = rs[0]
                            species.append(taxid)           
                    else:
                        continue
                print(f"species:{species}")
            except:
                print("fail at parsing ptc...")

        for specie in species:
            for gene in ptc_genes:
                try:
                    cur = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(specie,gene))
                except:
                    print(f"syntax error at {gene}. loop continue..")
                    continue
                rs = cur.fetchone()
                if rs == None:
                    print("No answer at pubtator for {} and {}".format(specie,gene))
                    pass
                else:
                    geneid = rs[0]
                    data_list.append({"#tax_id": specie, "GeneID": geneid, "PubMed_ID": pmid})
                    tmp2.append({"#tax_id": specie, "GeneID": geneid, "PubMed_ID": pmid})
                    print({"#tax_id": specie, "GeneID": geneid, "PubMed_ID": pmid})

        if tmp2 == [] and species != []:
            data_list.append({"#tax_id": species[0], "GeneID": "NotFound", "PubMed_ID": pmid})
            print({"#tax_id": species[0], "GeneID": "NotFound", "PubMed_ID": pmid})
            try:
                data_list.append({"#tax_id": species[1], "GeneID": "NotFound", "PubMed_ID": pmid})
                print({"#tax_id": species[1], "GeneID": "NotFound", "PubMed_ID": pmid})
            except:
                print("Only one taxonomy obtained in species_list. Loop continue..")
                continue           
        else:
            print("no species or genes found for this pmid. loop continue..")
            continue

# process pmids only
# 100 PMIDs for each access in PubTator
pmids2 = con.execute("select pmid from pubdetails where pmcid = 'Not found'")
pmidsonly = pmids2.fetchall()

pmids_only = []
for x in pmidsonly:
    pmids_only.append(x[0])

print(f"The number of pmids_only: {len(pmids_only)}")

list_of_chunked_pmids = generate_chunked_id_list(pmids_only, 100)
for a_chunked_pmids in list_of_chunked_pmids:
    pmids_str = ",".join(a_chunked_pmids)
    pt_url = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/biocxml?pmids={pmids_str}"
    # print(pt_url)
    try:
        tree_pubtator = use_eutils(pt_url)
    except:
        print(f"pubtator api error at {pt_url}. loop continue..")
        continue

    for element in tree_pubtator.findall("./document"):
        pmid = element.find("id").text
        print(f"\npmid:{pmid}....")
        taxids = []
        tmp = []
        pt_genes = []
        pmcid_cur = con.execute(f"select pmcid from pubdetails where pmid = '{pmid}'")
        pmcid = pmcid_cur.fetchone()[0]
        substances_cur = con.execute(f"select substances from pubdetails where pmid = '{pmid}'")
        substances = substances_cur.fetchone()[0]
        # pmcid = pmid_row["pmcid"].values[0]
        # substances = pmid_row["substances"].values[0]
        mesh_cur = con.execute(f"select mesh from pubdetails where pmid = '{pmid}'")
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
                        print(f"error at obtaining taxid for {taxname} from substances")
                        pass
                    else:
                        taxid = rs[0]
                    gene = protein.split()[0]
                    cur2 = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(taxid,gene))
                    rs2 = cur2.fetchone()
                    if rs2 == None:
                        print(f"error at obtaining substance_gene for {gene}")
                        pass
                    else:
                        geneid = rs2[0]
                except:
                    print(f"syntax error at substances. loop continue")
                    continue
                data_list.append({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})
                tmp.append({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})
                print(({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid}))

        # 2. check mesh for species extraction
        if mesh_list != []:
            try:
                for a_mesh in mesh_list:
                    cur = con.execute(f"select mesh_number from mtree where mesh_term = '{a_mesh}'")
                    rs = cur.fetchone()
                    if rs == None:
                        print(f"error at obtaining mesh_number for {a_mesh} from MESH")
                        pass
                    else:
                        treeid = rs[0]

                    # ↓ review reuqired
                    # # select if Amphibians
                    # if treeid.startswith("B01.050.150.900.090"):
                    #     species_category.append({"pmid": pmid, "species_category": "Amphibians"})
                    #     print({"pmid": pmid, "species_category": "Amphibians"})
                    # # select if Birds
                    # if treeid.startswith("B01.050.150.900.248"):
                    #     species_category.append({"pmid": pmid, "species_category": "Birds"})
                    #     print({"pmid": pmid, "species_category": "Birds"})
                    # # select if Fishes
                    # if treeid.startswith("B01.050.150.900.493"):
                    #     species_category.append({"pmid": pmid, "species_category": "Fishes"})
                    #     print({"pmid": pmid, "species_category": "Fishes"})
                    # # select if Mammals
                    # if treeid.startswith("B01.050.150.900.649"):
                    #     species_category.append({"pmid": pmid, "species_category": "Mammals"})
                    #     print({"pmid": pmid, "species_category": "Mammals"})
                    # # select if Reptiles
                    # if treeid.startswith("B01.050.150.900.833"):
                    #     species_category.append({"pmid": pmid, "species_category": "Reptiles"})
                    #     print({"pmid": pmid, "species_category": "Reptiles"})
                    # # select if Reptiles
                    # if treeid.startswith("B01.050.500.131.617"):
                    #     species_category.append({"pmid": pmid, "species_category": "Insecta"})
                    #     print({"pmid": pmid, "species_category": "Insecta"})

                    if treeid.startswith("B") and len(treeid.split('.')) > 5:
                        cur2 = con.execute(f"select tax_id from taxonomy where tax_name like '{a_mesh}'")
                        rs2 = cur2.fetchone()
                        if rs2 == None:
                            print(f"error at obtaining taxid for {a_mesh} from MESH")
                            pass
                        else:
                            taxid = rs2[0]
                            taxids.append(taxid)
            except:
                print("error around mesh scripts")
        else:
            pass

        if tmp != []:
            print("already obtained gene and specie. loop continue..")
            continue
        else:
            tmp2 =[]
            species = pubtator_species_from_pmid(element)
            genes = pubtator_genes_from_pmid(element)
            try:
                genes_count = collections.Counter(genes).most_common(20)
                print(f"genes_count:{genes_count}")
                for gene_count in genes_count:
                    # Extraction of genes that have been text mined more than 5 times from RESULTS or ABSTRACT
                    if gene_count[1] > 1:
                        pt_genes.append(gene_count[0])
                    else:
                        continue
                print(f"pt_genes:{pt_genes}")
                species_count = collections.Counter(species).most_common(20)
                print(f"species_count:{species_count}")
                for specie_count in species_count:
                    # Extraction of genes that have been text mined more than 10 times from METHODS or ABSTRACT
                    if specie_count[1] > 1:
                        taxname = specie_count[0]
                        # print(taxname)
                        cur = con.execute(f"select tax_id from taxonomy where tax_name like '{taxname}'")
                        rs = cur.fetchone()
                        if rs == None:
                            pass
                        else:
                            taxid = rs[0]
                            taxids.append(taxid)           
                    else:
                        continue
                print(f"species:{taxids}")
            except:
                print("fail at parsing pt...")
                continue

            for taxid in taxids:
                for gene in pt_genes:
                    try:
                        cur = con.execute("select GeneID from gene_info where tax_id = '{}' and UPPER(Symbol) like UPPER('{}')".format(taxid,gene))
                    except:
                        print(f"syntax error at {gene}. loop continue..")
                        continue
                    rs = cur.fetchone()
                    if rs == None:
                        print("No answer at pubtator for {} and {}".format(taxid,gene))
                        pass
                    else:
                        geneid = rs[0]
                        data_list.append({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})
                        tmp2.append({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})
                        print({"#tax_id": taxid, "GeneID": geneid, "PubMed_ID": pmid})

            if tmp2 == [] and taxids != []:
                data_list.append({"#tax_id": taxids[0], "GeneID": "NotFound", "PubMed_ID": pmid})
                print({"#tax_id": taxids[0], "GeneID": "NotFound", "PubMed_ID": pmid})
                try:
                    data_list.append({"#tax_id": taxids[1], "GeneID": "NotFound", "PubMed_ID": pmid})
                    print({"#tax_id": taxids[1], "GeneID": "NotFound", "PubMed_ID": pmid})
                except:
                    print("Only one taxonomy obtained in species_list. loop continue..")
                    continue             
            else:
                print("no species or genes found for this pmid. loop continue..")
                continue

# with open(f"/Users/suzuki/gem/csv_gitignore/20221215_species_categories.json", "w") as f:
#     json.dump(species_category, f, indent=3)

df_g2p = pd.read_csv("../csv_gitignore/gene2pubmed.tsv", sep="\t")
df_new = pd.DataFrame(data=data_list)
print(df_new.head())
df_g2p_updated = pd.concat([df_g2p, df_new])
df_g2p_updated.to_csv(f"../csv_gitignore/20221215_g2p_updated.csv")

con.close()