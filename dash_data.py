import json
from json import tool
from multiprocessing.sharedctypes import Value
import sqlite3
import pandas as pd
import dash_table


def data_for_fig1(DATABASE):
    list = []
    con = sqlite3.connect(DATABASE)
    tools = [
        "CRISPR-Cas9",
        "TALEN",
        "ZFN",
        "CRISPR-Cas12",
        "CRISPR-Cas3",
        "Base editor",
        "Prime editor",
    ]
    for tool in tools:
        # print(f"tool name:{tool}")
        for i in range(2010, 2023):
            # print(f"publication year:{i}")
            cur = con.execute(
                "select count(distinct pmid) from metadata221017 where pubdate like '{}%' and getool = '{}' ".format(
                    i, tool
                )
            )
            for row in cur:
                pub_number = row[0]
                list.append([str(i), tool, pub_number])
    con.close()
    return list


def data_for_fig4(DATABASE):
    ngslist = []
    con = sqlite3.connect(DATABASE)
    tools = [
        "CRISPR-Cas9",
        "TALEN",
        "ZFN",
        "CRISPR-Cas12",
        "CRISPR-Cas3",
        "Base editor",
        "Prime editor",
    ]
    for tool in tools:
        biopro_cur = con.execute(
            f"select count(distinct pmid) from metadata221017 where biopro_id like '[PRJ%' and getool = '{tool}' "
        )
        rna_cur = con.execute(
            f"select count(distinct pmid) from metadata221017 where RNA_seq like '[GSE%' and getool = '{tool}' "
        )
        for row in biopro_cur:
            count = row[0]
            ngslist.append([tool, "BioProject_ID", count])
        for row in rna_cur:
            count = row[0]
            ngslist.append([tool, "RNA_seq_ID", count])
    con.close()
    return ngslist


def data_for_fig2_right(DATABASE):
    list2 = []
    con = sqlite3.connect(DATABASE)
    cur = con.execute("select distinct taxonomyname from fig2 order by entries desc")
    pre_species_list = cur.fetchall()
    allspecies = []
    for x in pre_species_list:
        allspecies.append(x[0])
    # tax_csv = pd.read_csv("./csv/tax_list.csv")
    # tax_list = tax_csv["organism_name"].to_list()
    tax_list = allspecies[:20]
    tools = [
        "TALEN",
        "ZFN",
        "CRISPR-Cas12",
        "CRISPR-Cas3",
        "Base editor",
        "Prime editor",
    ]
    for tool in tools:
        for specie in tax_list:
            cur = con.execute(
                "select count(distinct genesymbol) from metadata221017 where organism_name = '{}' and getool = '{}' ".format(
                    specie, tool
                )
            )
            for row in cur:
                counts = row[0]
                # print(counts)
                list2.append([tool, specie, counts])
    con.close()
    return list2


def data_for_fig2_left(DATABASE):
    list3 = []
    con = sqlite3.connect(DATABASE)
    cur = con.execute("select distinct taxonomyname from fig2 order by entries desc")
    pre_species_list = cur.fetchall()
    allspecies = []
    for x in pre_species_list:
        allspecies.append(x[0])
    # tax_csv = pd.read_csv("./csv/tax_list.csv")
    # tax_list = tax_csv["organism_name"].to_list()
    tax_list = allspecies[:20]
    for specie in tax_list:
        cur = con.execute(
            f"select count(distinct genesymbol) from metadata221017 where organism_name = '{specie}' and getool = 'CRISPR-Cas9' "
        )
        for row in cur:
            counts = row[0]
            # print(counts)
            list3.append(["CRISPR-Cas9", specie, counts])
    con.close()
    return list3


# def data_for_ngsfig(DATABASE):
#     ngs_list = []
#     con = sqlite3.connect(DATABASE)
#     tools = [
#         "TALEN",
#         "ZFN",
#         "CRISPR-Cas12",
#         "CRISPR-Cas3",
#         "Base editor",
#         "Prime editor",
#     ]
#     for tool in tools:
#         cur_rna = con.execute(f"select count(*) from GEM_metadata where rna_seq != None and getool ='{}'")


def parse_callback_json_fig1(selectedData, DATABASE):
    json_content = selectedData["points"][0]
    if json_content["curveNumber"] == 0:
        tool = "CRISPR-Cas9"
    if json_content["curveNumber"] == 1:
        tool = "TALEN"
    if json_content["curveNumber"] == 2:
        tool = "ZFN"
    if json_content["curveNumber"] == 3:
        tool = "CRISPR-Cas12"
    if json_content["curveNumber"] == 4:
        tool = "CRISPR-Cas3"
    if json_content["curveNumber"] == 5:
        tool = "Base editor"
    if json_content["curveNumber"] == 6:
        tool = "Prime editor"
    year = json_content["x"]
    # print(tool)
    # print(year)
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata221017 where pubdate like '{}%' and getool = '{}'".format(
            year, tool
        ),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(columns={"getool":"Genome Editing Tool", "pmid":"PubMed ID", "pubtitle":"Publication Title", "pubdate":"Published Date", "organism_name":"Organism Name", "genesymbol":"GeneSymbol", "editing_type":"Editing Type", "gene_counts":"How much the Gene Studied", "biopro_id":"BioProject ID", "RNA_seq":"RNA-seq ID (GEO)", "vector":"Used Vector", "cellline":"Cell line", "tissue":"Tissue type", "Mutation_type":"Mutation Type"})
    con.close()
    return df


def parse_callback_json_fig2_left(selectedData, DATABASE):
    df_fig3s = pd.read_csv("./csv/tax_list_fig3s.csv")
    json_content = selectedData["points"][0]
    taxno = json_content["curveNumber"]
    row = df_fig3s[df_fig3s.iloc[:,0] == int(taxno)]
    # print(row)
    specie = row["species"].values[0]
    tool = json_content["x"]
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata221017 where organism_name = '{}' and getool = '{}'".format(
            specie, tool
        ),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(columns={"getool":"Genome Editing Tool", "pmid":"PubMed ID", "pubtitle":"Publication Title", "pubdate":"Published Date", "organism_name":"Organism Name", "genesymbol":"GeneSymbol", "editing_type":"Editing Type", "gene_counts":"How much the Gene Studied", "biopro_id":"BioProject ID", "RNA_seq":"RNA-seq ID (GEO)", "vector":"Used Vector", "cellline":"Cell line", "tissue":"Tissue type", "Mutation_type":"Mutation Type"})
    con.close()
    return df

def parse_callback_json_fig2_right(selectedData, DATABASE):
    df_fig2s = pd.read_csv("./csv/tax_list_fig2s.csv")
    json_content = selectedData["points"][0]
    taxno = json_content["curveNumber"]
    row = df_fig2s[df_fig2s.iloc[:,0] == int(taxno)]
    # print(row)
    specie = row["species"].values[0]
    tool = json_content["x"]
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata221017 where organism_name = '{}' and getool = '{}'".format(
            specie, tool
        ),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(columns={"getool":"Genome Editing Tool", "pmid":"PubMed ID", "pubtitle":"Publication Title", "pubdate":"Published Date", "organism_name":"Organism Name", "genesymbol":"GeneSymbol", "editing_type":"Editing Type", "gene_counts":"How much the Gene Studied", "biopro_id":"BioProject ID", "RNA_seq":"RNA-seq ID (GEO)", "vector":"Used Vector", "cellline":"Cell line", "tissue":"Tissue type", "Mutation_type":"Mutation Type"})
    con.close()
    return df


def parse_callback_json_fig4(selectedData, DATABASE):
    con = sqlite3.connect(DATABASE)
    json_content = selectedData["points"][0]
    ngsno = json_content["curveNumber"]
    tool = json_content["x"]
    if ngsno == 0:
        sql_query = pd.read_sql_query(
            f"select * from metadata221017 where biopro_id like '[PRJ%' and getool = '{tool}'",
            con,
        )
    if ngsno == 1:
        sql_query = pd.read_sql_query(
            f"select * from metadata221017 where RNA_seq like '[GSE%' and getool = '{tool}'",
            con,
        )

    df = pd.DataFrame(sql_query)
    con.close()
    return df


def selected_table(df_selected_fig1):
    table_selecteddata = dash_table.DataTable(
        id="table_selecteddata",
        style_cell={
            "textAlign": "center",
            "whiteSpace": "normal",
            "fontSize": 10,
        },
        style_table={
            "minWidth": "100%",
        },
        columns=[
            {
                "name": i,
                "id": j,
                "presentation": "markdown",
            }
            for i, j in zip(df_selected_fig1, df_selected_fig1.columns)
        ],
        data=df_selected_fig1.to_dict("records"),
        page_size=20,
        sort_action="native",
        filter_action="native",
        export_format="csv",
        style_as_list_view=True,
    )
    return table_selecteddata

def parse_callback_json_specie(value, DATABASE):
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(f"select * from metadata221017 where organism_name = '{value}'",con)
    df = pd.DataFrame(sql_query)
    df = df.rename(columns={"getool":"Genome Editing Tool", "pmid":"PubMed ID", "pubtitle":"Publication Title", "pubdate":"Published Date", "organism_name":"Organism Name", "genesymbol":"GeneSymbol", "editing_type":"Editing Type", "gene_counts":"How much the Gene Studied", "biopro_id":"BioProject ID", "RNA_seq":"RNA-seq ID (GEO)", "vector":"Used Vector", "cellline":"Cell line", "tissue":"Tissue type", "Mutation_type":"Mutation Type"})
    con.close()
    return df


def specie_selected_table(df_species):
    specie_selecteddata = dash_table.DataTable(
        id="specie_selecteddata",
        style_cell={
            "textAlign": "center",
            "whiteSpace": "normal",
            "fontSize": 10,
        },
        style_table={
            "minWidth": "100%",
        },
        columns=[
            {
                "name": i,
                "id": j,
                "presentation": "markdown",
            }
            for i, j in zip(df_species, df_species.columns)
        ],
        data=df_species.to_dict("records"),
        page_size=20,
        sort_action="native",
        filter_action="native",
        export_format="csv",
        style_as_list_view=True,
    )
    return specie_selecteddata

# selectedData = {
#     "points": [
#         {
#             "curveNumber": 20,
#             "pointNumber": 0,
#             "pointIndex": 0,
#             "x": "CRISPR-Cas9",
#             "y": 25367,
#             "label": "CRISPR-Cas9",
#             "value": 25367,
#         }
#     ]
# }
# DATABASE = "./data/0917_gem_test.db"

# df = parse_callback_json_fig2(selectedData, DATABASE)
# print(df.head())
