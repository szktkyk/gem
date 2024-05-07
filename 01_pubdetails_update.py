#TODO: requestsのエラーハンドリング必要そう？

from modules import eutils
import config
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # # 現状のPMIDリストを取得
    with open(config.old_pubdetails) as file:
        last_pmids_list = file.read().splitlines() 
    
    # 新しいPMIDリストを取得
    years_list = [str(x) for x in range(1990, 2024)]  
    new_pmids_list = []
    for year in years_list:
        year = int(year)
        id_res = eutils.call_esearch(config.search_query, year)
        for id in id_res.findall("./IdList/Id"):
            pmid = id.text
            new_pmids_list.append(pmid)
    new_pmids_list = list(set(new_pmids_list))
    print(f"number of pmids: {len(new_pmids_list)}")
    with open(f"./data/publication_details/{config.date}_pmidlist.txt",'w') as file:
        for item in new_pmids_list:
            file.write(item + '\n')


    # 更新するPMIDリストを取得
    set1 = set(new_pmids_list)
    set2 = set(last_pmids_list)
    update_pmid = list(set1.difference(set2))
    print(f"number of pmids to update: {len(update_pmid)}")


    pmids_metadata = get_pubdetails(update_pmid, 190)
    field_name = [
        "pmid",
        "doi",
        "pmcid",
        "title",
        "pubdate",
        "substances",
        "keyword",
        "abstract",
        "mesh",
        "getools"
    ]

    with open(f"./data/publication_details/{config.date}_pubdetails.csv", "w",) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(pmids_metadata)


def get_pubdetails(pmids:list, max_len:int):
    """
    Parameters:
    --------
    pmids: list
        a list of pmids

    max_len: int
        Number of elements in the list after splitting

    Returns:
    -------
    pmids_metadata:list
        a list containing dicts of publication details

    """
    list_of_chunked_pmids = eutils.generate_chunked_id_list(pmids, max_len)
    pmids_metadata = []
    for a_chunked_pmids in list_of_chunked_pmids:
        pmid_str = ",".join(a_chunked_pmids)
        epost_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pubmed&id={}&api_key={}"
        api1 = epost_params.format(pmid_str, os.getenv("api_key"))
        print(api1)
        print("connected to epost...")
        try:
            tree1 = eutils.use_eutils(api1)
            webenv = ""
            webenv = tree1.find("WebEnv").text
        except:
            print(f"error at {api1}")
            continue
        
        esummary_params = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&WebEnv={}&query_key=1&api_key={}&retmode=xml"
        api2 = esummary_params.format(webenv, os.getenv("api_key"))
        print("connected to efetch...")
        print(api2)
        try:
            tree2 = eutils.use_eutils(api2)
        except:
            print("error at {}".format(api2))
            continue

        for element in tree2.iter("PubmedArticle"):

            pmid = eutils.get_text_by_tree("./MedlineCitation/PMID", element)
            doiid = eutils.get_text_by_tree(
                "./PubmedData/ArticleIdList/ArticleId[@IdType='doi']",
                element,
            )
            pmcid = eutils.get_text_by_tree(
                "./PubmedData/ArticleIdList/ArticleId[@IdType='pmc']",
                element,
            )
            if pmcid == "":
                pmcid = "Not found"

            element_title = element.find("./MedlineCitation/Article/ArticleTitle")
            title = "".join(element_title.itertext())
            try:
                pubdate_year = element.find(
                    "./MedlineCitation/Article/ArticleDate/Year"
                ).text
                pubdate_month = element.find(
                    "./MedlineCitation/Article/ArticleDate/Month"
                ).text
                pubdate_day = element.find(
                    "./MedlineCitation/Article/ArticleDate/Day"
                ).text
            except:
                pubdate_year = element.find(
                    "./PubmedData/History/PubMedPubDate/Year"
                ).text
                pubdate_month = element.find(
                    "./PubmedData/History/PubMedPubDate/Month"
                ).text
                pubdate_day = element.find(
                    "./PubmedData/History/PubMedPubDate/Day"
                ).text

            pubdate = "{}-{}-{}".format(pubdate_year, pubdate_month, pubdate_day)

            substances_list = []
            substances = element.findall(
                "MedlineCitation/ChemicalList/Chemical/NameOfSubstance"
            )
            for substance in substances:
                substances_list.append(substance.text)

            keywords = []
            keywordlist = element.findall("MedlineCitation/KeywordList/Keyword")
            for keyword in keywordlist:
                if keyword.text != None:
                    a_keyword = keyword.text
                    a_keyword = a_keyword.replace('\n','')
                    a_keyword = a_keyword.replace(' ','')
                    keywords.append(a_keyword)
                else:
                    a_keyword = keyword.find("i").text
                    keywords.append(a_keyword)             
            try:
                keyword_str = ",".join(keywords)
            except:
                keyword_str = ""
                print(f"error at keywords:{keywords}")
                pass
            
            abstract_list = []
            element_abstract = element.findall(
                "./MedlineCitation/Article/Abstract/AbstractText"
            )
            for abstract in element_abstract:
                text = "".join(abstract.itertext())
                abstract_list.append(text)
            abstract = " ".join(abstract_list)

            mesh_list = []
            mesh_elements = element.findall(
                "./MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName"
            )
            for mesh in mesh_elements:
                mesh_list.append(mesh.text)

            getools = []
            for parse_pattern in config.parse_patterns.items():
                if parse_pattern[1].search(title):
                    # print(parse_pattern[1].search(title))
                    getools.append(parse_pattern[0])

                if parse_pattern[1].search(abstract):
                    # print(parse_pattern[1].search(abstract))
                    getools.append(parse_pattern[0])
                
                if parse_pattern[1].search(keyword_str):
                    # print(parse_pattern[1].search(abstract))
                    getools.append(parse_pattern[0])
            getools = list(set(getools))
            pmids_metadata.append(
                {
                    "pmid": pmid,
                    "doi": doiid,
                    "pmcid": pmcid,
                    "title": title,
                    "pubdate": pubdate,
                    "substances": substances_list,
                    "keyword": keyword_str,
                    "abstract": abstract,
                    "mesh": mesh_list,
                    "getools": getools,
                }
            )
            


    return pmids_metadata



if __name__ == "__main__":
    main()