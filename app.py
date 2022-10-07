import json
import sqlite3
import pandas as pd

from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
from dash_data import *


DATABASE = "./data/20220917/20220917_gem.db"

app = Dash(__name__)


colors = {"background": "#EFEFEF", "text": "#000000"}

# title = (
#     dcc.Markdown(
#         """
# ## *GEM: Genome Editing Meta-database*
# *Metadata extracted from PubMed Central, PubTator Central, NCBI gene*
# """
#     ),
# )
title_html = html.Div(
    [
        html.H3(
            "GEM: Genome Editing Meta-database",
            style={"fontSize": 25, "textAlign": "left"},
        ),
        html.P(
            "Metadata extracted from PubMed Central, PubTator Central, NCBI gene",
        ),
    ],
    style={
        "width": "48%",
        "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)

title_right_html = html.Div(
    [
        html.P(
            "last updated: 2022-Sep-17",
            style={"fontSize": 20, "textAlign": "right"},
        ),
        html.A("About/How to use", href="/assets/about.html", target="_blank"),
        html.P(""),
        html.A("News", href="/assets/news.html", target="_blank"),
        html.P(""),
        html.A(
            "Bonohulab/Contact",
            href="https://bonohu.hiroshima-u.ac.jp/index_en.html",
            target="_blank",
        ),
    ],
    style={
        "width": "45%",
        "margin": "2%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "right",
    },
)


list = data_for_fig1(DATABASE)
df = pd.DataFrame(
    data=list,
    columns=["publication year", "genome editing tools", "the number of literatures"],
)

list2 = data_for_fig2_right(DATABASE)
df2 = pd.DataFrame(
    data=list2,
    columns=["genome editing tools", "species", "the number of genes studied"],
)
df2s = df2.sort_values("the number of genes studied",ascending=False)
df2s = df2s.reset_index()
df2s.to_csv("tax_list_fig2s.csv",columns=['species'],index=True)


list3 = data_for_fig2_left(DATABASE)
df3 = pd.DataFrame(
    data=list3,
    columns=["genome editing tools", "species", "the number of genes studied"],
)
df3s = df3.sort_values("the number of genes studied",ascending=False)
df3s = df3s.reset_index()
df3s.to_csv("tax_list_fig3s.csv",columns=['species'],index=True)

list4 = data_for_fig4(DATABASE)
df_fig4 = pd.DataFrame(
    data=list4,
    columns=["genome editing tools", "NGS ID type", "the number of literatures"],
)


df4 = pd.read_csv("20220917_ge_metadata.csv")
df4 = df4.rename(columns={"getool":"Genome Editing Tool", "pmid":"PubMed ID", "pubtitle":"Publication Title", "pubdate":"Published Date", "organism_name":"Organism Name", "genesymbol":"GeneSymbol", "editing_type":"Editing Type", "gene_counts":"How much the Gene Studied", "biopro_id":"BioProject ID", "RNA_seq":"RNA-seq ID (GEO)", "vector":"Used Vector", "cellline":"Cell line", "tissue":"Tissue type", "Mutation_type":"Mutation Type"})


external_stylesheets = ["https://codepen.io/chriddyp/pen/dWLwgP.css"]


firstfig = html.Div(
    [
        html.H1("browse by publication year", style={"fontSize": 20}),
        html.P("Please select the area on the figure below to retrive metadata"),
        dcc.Graph(
            id="fig1",
            figure=px.bar(
                df,
                x="publication year",
                y="the number of literatures",
                color="genome editing tools",
                template={"layout": {"clickmode": "event+select"}},
            ),
        ),
    ],
    style={
        "width": "49%",
        "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)

fig4 = html.Div(
    [
        html.H1("browse by NGS data availability", style={"fontSize": 20}),
        html.P("Please select the area on the figure below to retrive metadata"),
        dcc.Graph(
            id="fig4",
            figure=px.bar(
                df_fig4,
                x="genome editing tools",
                y="the number of literatures",
                color="NGS ID type",
                template={"layout": {"clickmode": "event+select"}},
            ),
        ),
    ],
    style={
        "width": "45%",
        "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)


fig1_output = html.Div(
    [
        html.P(id="fig1_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

fig4_output = html.Div(
    [
        html.P(id="fig4_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

second_figs_html = html.Div(
    [
        html.H1(
            "browse by species",
            style={"fontSize": 20, "textAlign": "left"},
        ),
        html.P(
            "Please select the area on the figure below to retrive metadata",
        ),
    ],
    style={
        # "width": "49%",
        "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)

second_left_fig = html.Div(
    [
        dcc.Graph(
            id="fig2_left",
            figure=px.bar(
                df3s,
                x="genome editing tools",
                y="the number of genes studied",
                color="species",
                template={"layout": {"clickmode": "event+select"}},
                # title="The number of genes studied by CRISPR-Cas9 for each specie",
            ),
        ),
    ],
    style={
        "width": "30%",
        # "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "right",
    },
)

second_right_fig = html.Div(
    [
        dcc.Graph(
            id="fig2_right",
            figure=px.bar(
                df2s,
                x="genome editing tools",
                y="the number of genes studied",
                color="species",
                template={"layout": {"clickmode": "event+select"}},
            ),
        ),
    ],
    style={
        "width": "60%",
        # "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)
fig2_output = html.Div(
    [
        html.P(id="fig2_output_div1", style={"fontSize": 15, "textAlign": "center"}),
        html.P(id="fig2_output_div2", style={"fontSize": 15, "textAlign": "center"}),
    ]
)


before_table_html = html.Div(
    [
        html.H1(
            "Dataset",
            style={"fontSize": 20, "textAlign": "left"},
        ),
    ],
    style={
        # "width": "49%",
        "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)

table = dash_table.DataTable(
    id="table",
    style_cell={
        "textAlign": "center",
        "whiteSpace": "normal",
        "fontSize": 12,
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
        for i, j in zip(df4, df4.columns)
    ],
    data=df4.to_dict("records"),
    page_size=50,
    sort_action="native",
    filter_action="native",
    export_format="csv",
    style_as_list_view=True,
)


license = html.Div(
    [
        html.Img(src="/assets/cc_by.png"),
        html.P(
            "This work is licensed under a Creative Commons Attribution 4.0 International License.",
            style={"fontSize": 20, "textAlign": "left"},
        ),
        html.A(
            "Contact us at bonohulab for any feedbacks",
            href="https://bonohu.hiroshima-u.ac.jp/index_en.html",
            target="_blank",
            style={"fontSize": 20, "textAlign": "left"},
        ),
    ],
    style={
        # "width": "49%",
        "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)

app.layout = html.Div(
    children=[
        html.Div([title_html, title_right_html]),
        html.Div([firstfig, fig4]),
        html.Div([fig1_output, fig4_output]),
        html.Div([second_figs_html]),
        html.Div([second_left_fig, second_right_fig]),
        html.Div([fig2_output]),
        html.Div([before_table_html]),
        html.Div([table]),
        html.Div([license]),
    ],
    style={"background": colors["background"], "color": colors["text"]},
)


@app.callback(
    Output("fig1_output_div", "children"),
    [Input("fig1", "selectedData")],
    prevent_initial_call=True,
)
def show_hover_data(selectedData):
    if selectedData is None:
        html.Div()
    else:
        # print(selectedData)
        df_selected_fig1 = parse_callback_json_fig1(selectedData, DATABASE)
        table_selected_fig1 = selected_table(df_selected_fig1)
        return table_selected_fig1


@app.callback(
    Output("fig4_output_div", "children"),
    [Input("fig4", "selectedData")],
    prevent_initial_call=True,
)
def CreateTableFig4(selectedData):
    if selectedData is None:
        html.Div()
    else:
        # print(selectedData)
        df_selected_fig4 = parse_callback_json_fig4(selectedData, DATABASE)
        table_selected_fig4 = selected_table(df_selected_fig4)
        return table_selected_fig4


@app.callback(
    Output("fig2_output_div1", "children"),
    [Input("fig2_left", "selectedData")],
    prevent_initial_call=True,
)
def CreateTableFig2Left(selectedData):
    if selectedData:
        df_selected_fig2 = parse_callback_json_fig2_left(selectedData, DATABASE)
        table_selected_fig2_left = selected_table(df_selected_fig2)
        return table_selected_fig2_left
    else:
        html.Div()


@app.callback(
    Output("fig2_output_div2", "children"),
    [Input("fig2_right", "selectedData")],
    prevent_initial_call=True,
)
def CreateTableFig2Left(selectedData):
    if selectedData:
        df_selected_fig2 = parse_callback_json_fig2_right(selectedData, DATABASE)
        table_selected_fig2_right = selected_table(df_selected_fig2)
        return table_selected_fig2_right
    else:
        html.Div()


if __name__ == "__main__":
    app.run(port=8000, debug=True)
