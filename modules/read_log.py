import ast


def get_datalist_from_log02(logfilepath):
    extracted_genes = []
    extracted_disease = []
    extracted_tissue = []
    with open(logfilepath) as f:
        for line in f:
            if line.startswith("{'pmid':"):
                line_dict = ast.literal_eval(line)
                extracted_genes.append(line_dict)
            if line.startswith("{'disease':"):
                line_dict = ast.literal_eval(line)
                extracted_disease.append(line_dict)
            if line.startswith("{'tissue':"):
                line_dict = ast.literal_eval(line)
                extracted_tissue.append(line_dict)
            else:
                continue


    return extracted_genes, extracted_disease, extracted_tissue


def get_pmids_from_log02(logfilepath):
    pmids = []
    with open(logfilepath) as f:
        for line in f:
            if line.startswith("pmid:") and line.endswith("....\n"):
                pmid = line.split("pmid:")[1].split("....")[0]
                pmids.append(pmid)
            else:
                continue

    return pmids


def get_pmids_from_log03(logfilepath):
    pmids = []
    with open(logfilepath) as f:
        for line in f:
            if line.startswith("pmid...."):
                pmid = line.split("pmid....")[1].split("\n")[0]
                pmid = pmid.split(": ")[1]
                pmids.append(pmid)
            else:
                continue

    return pmids


def get_pmids_from_log_substances(logfilepath):
    """
    I wanted to put genes in tmp_genes when taxid was not obtained in substances, but I forgot to do so.
    So I created a function to get pmid from the log file.
    """
    pmids = []
    with open(logfilepath, 'r') as f:
        for block in process_block(f):
            for line in block:
                if line.startswith("pmid:") and line.endswith("....\n"):
                    pmid = line.split("pmid:")[1].split("....")[0]
                else:
                    pass
                if line.endswith("Go to next substances.\n") or line.endswith("Only gene is added to the tmp_genes\n"):
                    pmids.append(pmid)
                else:
                    pass
    return pmids                    


def process_block(f):
    block = []
    for line in f:
        if line.startswith('pmid:'):
            if block:
                yield block
            block = [line]
        elif line.strip() == '':
            block.append(line)
            yield block
            block = []
        else:
            block.append(line)
    if block:
        yield block




