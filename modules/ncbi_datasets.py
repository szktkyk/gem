import subprocess
import json
import requests

def get_taxid_from_taxname(taxname):
    req1 = subprocess.run(
        ["datasets", "summary", "taxonomy", "taxon", "{}".format(taxname)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        req_tax = json.loads(req1.stdout.decode())
        if req_tax["total_count"] == 0:
            print("no taxid from taxname found..")
            taxid = "NotFound"
        else:
            taxid = req_tax["reports"][0]["taxonomy"]["tax_id"]
    except:
        print("error at taxid from taxname..")
        taxid = "NotFound"
    return taxid

def get_taxname_from_taxid(taxid):
    req1 = subprocess.run(
        ["datasets", "summary", "taxonomy", "taxon", "{}".format(taxid), "--report", "names"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    req_tax = json.loads(req1.stdout.decode())
    try:
        if req_tax["total_count"] == 0:
            print("no taxname from taxid found..")
            taxname = taxid
        else:
            taxname = req_tax["reports"][0]["taxonomy"]["current_scientific_name"]["name"]
    except:
        print("error at taxname from taxid..")
        taxname = taxid
    return taxname

def get_geneid_from_genesymbol(gene_name, taxid):
    req2 = subprocess.run(
        ["datasets", "summary", "gene", "symbol", "{}".format(gene_name), "--taxon", "{}".format(taxid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        req_gene = json.loads(req2.stdout.decode())
        if req_gene["total_count"] == 0:
            print("no geneid from genesymbol..")
            geneid = "NotFound"
        else:
            geneid = req_gene["reports"][0]["gene"]["gene_id"]
    except:
        print("error at geneid from genesymbol...")
        geneid = "NotFound"

    return geneid

def get_genesymbol_from_geneid(geneid):
    req2 = subprocess.run(
        ["datasets", "summary", "gene", "gene-id", "{}".format(geneid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    req_gene = json.loads(req2.stdout.decode())
    if req_gene["total_count"] == 0:
        print("no genesymbol from geneid...")
        genesymbol = "NotFound"
    else:
        # print(req_gene)
        genesymbol = req_gene["reports"][0]["gene"]["symbol"]
    return genesymbol

def get_taxid_from_geneid(geneid):
    req2 = subprocess.run(
        ["datasets", "summary", "gene", "gene-id", "{}".format(geneid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    req_gene = json.loads(req2.stdout.decode())
    if req_gene["total_count"] == 0:
        print("no taxid from geneid...")
        taxid = "NotFound"
    elif "warning" in req_gene["reports"][0] and req_gene["reports"][0]["warning"]:
        print(req_gene)
        print("no taxid from geneid...")
        taxid = "NotFound"
    else:
        taxid = req_gene["reports"][0]["gene"]["tax_id"]
    return taxid

def ensg2ncbi(ensg):
    r = requests.post(
    url='https://biit.cs.ut.ee/gprofiler/api/convert/convert/',
    json={
        'organism':'hsapiens',
        'target':'ENTREZGENE_ACC',
        'query':ensg,
    }
    )
    resultlist = r.json()['result']
    ncbigeneid = resultlist[0]['converted']
    return ncbigeneid