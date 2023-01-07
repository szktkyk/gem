import ast
import pandas as pd
import datetime



# t_delta = datetime.timedelta(hours=9)
# JST = datetime.timezone(t_delta, "JST")
# now = datetime.datetime.now(JST)
# date = now.strftime("%Y%m%d")
# date = "20221215"
# df_pubdetails = pd.read_csv(
#     f"/Users/suzuki/gem/data/20221214/20221214_pubdetails.csv", sep=","
# )
# pmids = df_pubdetails["pmid"].tolist()

def get_datalist_from_log(logfilepath):
    data_list = []
    pmid_list = []
    with open(logfilepath) as f:
        for line in f:
            if line.startswith("{'getool"):
                line_dict = ast.literal_eval(line)
                data_list.append(line_dict)
            
            if line.startswith("pmid....:"):
                splited = line.split(":")
                pmid = splited[1]
                pmid_int = int(pmid)
                pmid_list.append(pmid_int)

    return data_list,pmid_list



# logfilepath1 = "../log/20221216_W04_log.txt"
# data_list, pmid_list = get_datalist_from_log(logfilepath1)
# # print(len(pmids))
# # print(len(data_list))
# # print(len(pmid_list))
# todopmid = list(set(pmids) - set(pmid_list))
# # print(len(todopmid))


