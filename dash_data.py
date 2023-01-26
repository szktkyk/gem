import json
from json import tool
from multiprocessing.sharedctypes import Value
import sqlite3
import pandas as pd
import dash_table

date = "20230125"


def data_for_searchbypub(DATABASE):
    list_searchbypub = []
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
        for i in range(2010, 2024):
            # print(f"publication year:{i}")
            cur = con.execute(
                "select count(distinct pmid) from metadata{} where pubdate like '{}%' and getool = '{}' ".format(
                    date, i, tool
                )
            )
            for row in cur:
                pub_number = row[0]
                list_searchbypub.append([str(i), tool, pub_number])
    con.close()
    return list_searchbypub


def data_for_searchbyngs(DATABASE):
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
            "select count(distinct pmid) from metadata{} where biopro_id like '[PRJ%' and getool = '{}' ".format(
                date, tool
            )
        )
        rna_cur = con.execute(
            "select count(distinct pmid) from metadata{} where RNA_seq like '[GSE%' and getool = '{}' ".format(
                date, tool
            )
        )
        for row in biopro_cur:
            count = row[0]
            ngslist.append([tool, "BioProject_ID", count])
        for row in rna_cur:
            count = row[0]
            ngslist.append([tool, "RNA_seq_ID", count])
    con.close()
    return ngslist


def data_for_speciesfig_right(DATABASE):
    list_speciesfig_right = []
    con = sqlite3.connect(DATABASE)
    cur = con.execute(
        "select distinct taxonomyname from fig2 order by entries desc"
    )
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
                "select count(distinct genesymbol) from metadata{} where organism_name = '{}' and getool = '{}' ".format(
                    date, specie, tool
                )
            )
            for row in cur:
                counts = row[0]
                # print(counts)
                list_speciesfig_right.append([tool, specie, counts])
    con.close()
    return list_speciesfig_right


def data_for_speciesfig_left(DATABASE):
    list_speciesfig_left = []
    con = sqlite3.connect(DATABASE)
    cur = con.execute(
        "select distinct taxonomyname from fig2 order by entries desc"
    )
    pre_species_list = cur.fetchall()
    allspecies = []
    for x in pre_species_list:
        allspecies.append(x[0])
    # tax_csv = pd.read_csv("./csv/tax_list.csv")
    # tax_list = tax_csv["organism_name"].to_list()
    tax_list = allspecies[:20]
    for specie in tax_list:
        cur = con.execute(
            "select count(distinct genesymbol) from metadata{} where organism_name = '{}' and getool = 'CRISPR-Cas9' ".format(
                date, specie
            )
        )
        for row in cur:
            counts = row[0]
            # print(counts)
            list_speciesfig_left.append(["CRISPR-Cas9", specie, counts])
    con.close()
    return list_speciesfig_left


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
        "select * from metadata{} where pubdate like '{}%' and getool = '{}'".format(
            date, year, tool
        ),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(
        columns={
            "getool": "Genome Editing Tool",
            "pmid": "PubMed ID",
            "pubtitle": "Publication Title",
            "pubdate": "Published Date",
            "taxonomy_category": "Taxonomy Category",
            "organism_name": "Organism Name",
            "genesymbol": "GeneSymbol",
            "editing_type": "Editing Type",
            "gene_counts": "How much the Gene Studied",
            "biopro_id": "BioProject ID",
            "RNA_seq": "RNA-seq ID (GEO)",
            "vector": "Used Vector",
            "cellline": "Cell line",
            "tissue": "Tissue type",
            "Mutation_type": "Mutation Type",
        }
    )
    con.close()
    return df


def parse_callback_json_fig2_left(selectedData, DATABASE):
    df_fig3s = pd.read_csv("./csv/tax_list_fig3s.csv")
    json_content = selectedData["points"][0]
    taxno = json_content["curveNumber"]
    row = df_fig3s[df_fig3s.iloc[:, 0] == int(taxno)]
    # print(row)
    specie = row["species"].values[0]
    tool = json_content["x"]
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata{} where organism_name = '{}' and getool = '{}'".format(
            date, specie, tool
        ),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(
        columns={
            "getool": "Genome Editing Tool",
            "pmid": "PubMed ID",
            "pubtitle": "Publication Title",
            "pubdate": "Published Date",
            "organism_name": "Organism Name",
            "genesymbol": "GeneSymbol",
            "editing_type": "Editing Type",
            "gene_counts": "How much the Gene Studied",
            "biopro_id": "BioProject ID",
            "RNA_seq": "RNA-seq ID (GEO)",
            "vector": "Used Vector",
            "cellline": "Cell line",
            "tissue": "Tissue type",
            "Mutation_type": "Mutation Type",
        }
    )
    con.close()
    return df


def parse_callback_json_fig2_right(selectedData, DATABASE):
    df_fig2s = pd.read_csv("./csv/tax_list_fig2s.csv")
    json_content = selectedData["points"][0]
    taxno = json_content["curveNumber"]
    row = df_fig2s[df_fig2s.iloc[:, 0] == int(taxno)]
    # print(row)
    specie = row["species"].values[0]
    tool = json_content["x"]
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata{} where organism_name = '{}' and getool = '{}'".format(
            date, specie, tool
        ),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(
        columns={
            "getool": "Genome Editing Tool",
            "pmid": "PubMed ID",
            "pubtitle": "Publication Title",
            "pubdate": "Published Date",
            "organism_name": "Organism Name",
            "genesymbol": "GeneSymbol",
            "editing_type": "Editing Type",
            "gene_counts": "How much the Gene Studied",
            "biopro_id": "BioProject ID",
            "RNA_seq": "RNA-seq ID (GEO)",
            "vector": "Used Vector",
            "cellline": "Cell line",
            "tissue": "Tissue type",
            "Mutation_type": "Mutation Type",
        }
    )
    con.close()
    return df


def parse_callback_json_fig4(selectedData, DATABASE):
    con = sqlite3.connect(DATABASE)
    json_content = selectedData["points"][0]
    ngsno = json_content["curveNumber"]
    tool = json_content["x"]
    if ngsno == 0:
        sql_query = pd.read_sql_query(
            "select * from metadata{} where biopro_id like '[PRJ%' and getool = '{}'".format(
                date, tool
            ),
            con,
        )
    if ngsno == 1:
        sql_query = pd.read_sql_query(
            "select * from metadata{} where RNA_seq like '[GSE%' and getool = '{}'".format(
                date, tool
            ),
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


def parse_callback_json_species(value, DATABASE):
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata{} where organism_name = '{}'".format(date, value), con
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(
        columns={
            "getool": "Genome Editing Tool",
            "pmid": "PubMed ID",
            "pubtitle": "Publication Title",
            "pubdate": "Published Date",
            "organism_name": "Organism Name",
            "genesymbol": "GeneSymbol",
            "editing_type": "Editing Type",
            "gene_counts": "How much the Gene Studied",
            "biopro_id": "BioProject ID",
            "RNA_seq": "RNA-seq ID (GEO)",
            "vector": "Used Vector",
            "cellline": "Cell line",
            "tissue": "Tissue type",
            "Mutation_type": "Mutation Type",
        }
    )
    con.close()
    return df


def parse_callback_json_taxonomy_category(value, DATABASE):
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        "select * from metadata{} where taxonomy_category = '{}'".format(date, value),
        con,
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(
        columns={
            "getool": "Genome Editing Tool",
            "pmid": "PubMed ID",
            "pubtitle": "Publication Title",
            "pubdate": "Published Date",
            "taxonomy_category": "Taxonomy Category",
            "organism_name": "Organism Name",
            "genesymbol": "GeneSymbol",
            "editing_type": "Editing Type",
            "gene_counts": "How much the Gene Studied",
            "biopro_id": "BioProject ID",
            "RNA_seq": "RNA-seq ID (GEO)",
            "vector": "Used Vector",
            "cellline": "Cell line",
            "tissue": "Tissue type",
            "Mutation_type": "Mutation Type",
        }
    )
    con.close()
    return df


def species_selected_table(df_species):
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


def taxonomy_category_selected_table(df_taxonomy_category):
    taxonomy_category_selecteddata = dash_table.DataTable(
        id="taxonomy_category_selecteddata",
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
            for i, j in zip(df_taxonomy_category, df_taxonomy_category.columns)
        ],
        data=df_taxonomy_category.to_dict("records"),
        page_size=20,
        sort_action="native",
        filter_action="native",
        export_format="csv",
        style_as_list_view=True,
    )
    return taxonomy_category_selecteddata


def data_for_species_fig(DATABASE, species):
    datalist = []
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
        cur = con.execute(
            "select count(distinct genesymbol) from metadata{} where organism_name = '{}' and getool = '{}' ".format(
                date, species, tool
            )
        )
        for row in cur:
            counts = row[0]
            # print(counts)
            datalist.append([tool, species, counts])
    con.close()
    return datalist


def data_for_taxonomy_category_fig(DATABASE, taxonomycategory):
    datalist = []
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
        cur = con.execute(
            "select count(distinct genesymbol) from metadata{} where taxonomy_category = '{}' and getool = '{}' ".format(
                date, taxonomycategory, tool
            )
        )
        for row in cur:
            counts = row[0]
            # print(counts)
            datalist.append([tool, taxonomycategory, counts])
    con.close()
    return datalist


def parse_callback_json_getools(value, DATABASE):
    con = sqlite3.connect(DATABASE)
    sql_query = pd.read_sql_query(
        f"select * from pmid_getools where getools = '{value}'", con
    )
    df = pd.DataFrame(sql_query)
    df = df.rename(
        columns={
            "pmid": "PubMed ID",
            "getool": "Genome Editing Tool",
            "pubtitle": "Publication Title",
            "biopro_id": "BioProject ID",
            "RNA_seq": "RNA-seq ID (GEO)",
            "vector": "Used Vector",
            "cellline": "Cell line",
            "editing_type": "Editing Type",
            "tissue": "Tissue type",
            "Mutation_type": "Mutation Type",
        }
    )
    con.close()
    return df


def getools_selected_table(df_getools):
    getools_selecteddata = dash_table.DataTable(
        id="getools_selecteddata",
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
            for i, j in zip(df_getools, df_getools.columns)
        ],
        data=df_getools.to_dict("records"),
        page_size=20,
        sort_action="native",
        filter_action="native",
        export_format="csv",
        style_as_list_view=True,
    )
    return getools_selecteddata


def getools_list(DATABASE):
    con = sqlite3.connect(DATABASE)
    cur = con.execute("select distinct getools from pmid_getools")
    getools_categories = [i[0] for i in cur.fetchall()]
    con.close()
    return getools_categories


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
