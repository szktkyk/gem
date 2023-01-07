import ast
import pandas as pd
import datetime


df_g2p = pd.read_csv("../csv_gitignore/gene2pubmed.tsv", sep="\t")
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, "JST")
now = datetime.datetime.now(JST)
date = now.strftime("%Y%m%d")


def get_datalist_from_log(logfilepath):
    data_list = []
    with open(logfilepath) as f:
        for line in f:
            if line.startswith("{'#tax_id"):
                line_dict = ast.literal_eval(line)
                data_list.append(line_dict)

    return data_list


# print(len(pmids))
# print(pmids.index("33432361"))
# new_pmids = pmids[9474:]
# print(new_pmids)
# exit()

logfilepath1 = "../log/20221214_W02_log.txt"
data_list1 = get_datalist_from_log(logfilepath1)
logfilepath2 = "../log/20221215_W02_log.txt"
data_list2 = get_datalist_from_log(logfilepath2)
data_list = data_list1 + data_list2

df_new = pd.DataFrame(data=data_list)
print(df_new)
df_g2p_updated = pd.concat([df_g2p, df_new])
df_g2p_updated.to_csv(f"../csv_gitignore/20221215_g2p_updated.csv")
exit()
