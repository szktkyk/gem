import json
import sqlite3
import pandas as pd

from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
from dash_data import *


DATABASE = "./data/gem.db"

app = Dash(__name__)
app.title = "GEM"
date = "20230125"

colors = {"background": "#EFEFEF", "text": "#000000"}


app.index_string = """
<!DOCTYPE html>
<html>
    <head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-246819650-1"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-246819650-1');
    </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

title_html = html.Div(
    [
        html.H3(
            "GEM: Genome Editing Meta-database",
            style={"fontSize": 25, "textAlign": "left"},
        ),
        html.P(
            "A Dataset of Genome Editing related Metadata extracted from PubMed literatures",
        ),
        html.P(
            "This is a web interface to Search and Retrieve metadata",
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
            f"last updated: {date}",
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
        # "margin": "2%",
        # "line-hight":"1",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "right",
    },
)


list_searchbypub = data_for_searchbypub(DATABASE)
df = pd.DataFrame(
    data=list_searchbypub,
    columns=["publication year", "genome editing tools", "the number of literatures"],
)

list_searchbyngs = data_for_searchbyngs(DATABASE)
df_fig4 = pd.DataFrame(
    data=list_searchbyngs,
    columns=["genome editing tools", "NGS ID type", "the number of literatures"],
)

list_speciesfig_right = data_for_speciesfig_right(DATABASE)
df2 = pd.DataFrame(
    data=list_speciesfig_right,
    columns=["genome editing tools", "species", "the number of genes studied"],
)
# df2s = df2.sort_values("the number of genes studied",ascending=False)
df2s = df2.reset_index()
df2s.to_csv("./csv/tax_list_fig2s.csv",columns=['species'],index=True)


list_speciesfig_left = data_for_speciesfig_left(DATABASE)
df3 = pd.DataFrame(
    data=list_speciesfig_left,
    columns=["genome editing tools", "species", "the number of genes studied"],
)
df3s = df3.sort_values("the number of genes studied",ascending=False)
df3s = df3s.reset_index()
df3s.to_csv("./csv/tax_list_fig3s.csv",columns=['species'],index=True)

# df4 = pd.read_csv(f"{date}_metadata.csv")
con = sqlite3.connect(DATABASE)
df4 = pd.read_sql_query(f'select * from metadata{date}',con)
df4 = df4.rename(columns={"getool":"Genome Editing Tool", "pmid":"PubMed ID", "pubtitle":"Publication Title", "pubdate":"Published Date","taxonomy_category":"Taxonomy Category", "organism_name":"Organism Name", "genesymbol":"GeneSymbol", "editing_type":"Editing Type", "gene_counts":"How much the Gene Studied", "biopro_id":"BioProject ID", "RNA_seq":"RNA-seq ID (GEO)", "vector":"Used Vector", "cellline":"Cell line", "tissue":"Tissue type", "Mutation_type":"Mutation Type"})
df4["How much the Gene Studied"] = df4["How much the Gene Studied"].astype('int',errors='ignore')
allspecies = df4['Organism Name'].unique().tolist()
# print(allspecies)
allcategories = df4['Taxonomy Category'].unique().tolist()
print(allcategories)

getools_categories = getools_list(DATABASE)
# print(getools_categories)

external_stylesheets = ["https://codepen.io/chriddyp/pen/dWLwgP.css"]


searchalldata_html = html.Div(
    [
        html.H1(
            "Search from all metadata",
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

alldata_html = html.Div(
    [
        html.Button(
            "SHOW WHOLE DATASET",
            style={"fontSize": 20, "textAlign": "left"},
            id='btn-nclicks-1',n_clicks=0),
        html.Button(
            "HIDE TABLE",
            style={"fontSize": 20, "textAlign": "left"},
            id='btn-nclicks-2',n_clicks=0)
    ],
    style={
        # "width": "49%",
        # "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)

alldata_output = html.Div(
    [
        html.P(id="wholedata_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

getools_html = html.Div(
    [
        html.H1(
            "Search by Genome editing tools",
            style={"fontSize": 20, "textAlign": "left"},
        ),
        html.P(
            "Please select a combination of genome editing tools from the dropdown options",
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

getools_output = html.Div(
    [
        html.P(id="getools_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

searchbypub_html = html.Div(
    [
        html.H1("Search by Publication Year", style={"fontSize": 20}),
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

searchbyngs_html = html.Div(
    [
        html.H1("Search by NGS data availability", style={"fontSize": 20}),
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


searchbypub_output = html.Div(
    [
        html.P(id="fig1_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

searchbyngs_output = html.Div(
    [
        html.P(id="fig4_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

taxonomy_category_html = html.Div(
    [
        html.H1(
            "Search by Taxonomy Categories",
            style={"fontSize": 20, "textAlign": "left"},
        ),
        html.P(
            "Please select a Taxonomy category from the dropdown options",
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

taxonomy_category_output = html.Div(
    [
        html.P(id="taxonomy_category_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)



species_html = html.Div(
    [
        html.H1(
            "Search by Species",
            style={"fontSize": 20, "textAlign": "left"},
        ),
        html.P(
            "Please select a specie from the dropdown options or select the area on the figure below to retrive metadata",
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

species_output = html.Div(
    [
        html.P(id="species_output_div", style={"fontSize": 15, "textAlign": "center"}),
    ]
)

speciesleft_fig = html.Div(
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
        "width": "40%",
        # "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "right",
    },
)

speciesright_fig = html.Div(
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
        "width": "55%",
        # "margin": "1%",
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "left",
    },
)
speciesfig_output = html.Div(
    [
        html.P(id="fig2_output_div1", style={"fontSize": 15, "textAlign": "center"}),
        html.P(id="fig2_output_div2", style={"fontSize": 15, "textAlign": "center"}),
    ]
)


table_output = html.Div(
    [
        html.P(id="table_output", style={"fontSize": 10, "textAlign": "center"}),
    ]
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
        html.Div([searchalldata_html]),
        html.Div([alldata_html]),
        html.Div([alldata_output]),
        html.Div([getools_html]),
        dcc.Dropdown(
            id="filter_dropdown_getools",
            options=[{"label":st,"value":st} for st in getools_categories],
            placeholder="-Select a combination of genome editing tools-",
            multi=False),
        html.Div([getools_output]),
        html.Div([searchbypub_html, searchbyngs_html]),
        html.Div([searchbypub_output, searchbyngs_output]),
        html.Div([taxonomy_category_html]),
        dcc.Dropdown(
            id="filter_dropdown2",
            options=[{"label":st,"value":st} for st in allcategories],
            placeholder="-Select a taxonomy category",
            multi=False
        ),
        html.Div([taxonomy_category_output]),
        html.Div([species_html]),
        dcc.Dropdown(
            id="filter_dropdown",
            options=[{"label":st,"value":st} for st in allspecies],
            placeholder="-Select a species-",
            multi=False),
        html.Div([species_output]),
        html.Div([table_output]),
        html.Div([speciesleft_fig, speciesright_fig]),
        html.Div([speciesfig_output]),
        html.Div([license]),
    ],
    style={"background": colors["background"], "color": colors["text"]},
)

@app.callback(
    Output('wholedata_output_div','children'),
    Input('btn-nclicks-1','n_clicks'),
    Input('btn-nclicks-2','n_clicks'),
    prevent_initial_call=True,
)
def displaytable(btn1,btn2):
    if "btn-nclicks-1" == ctx.triggered_id:
        table = dash_table.DataTable(
        id="table",
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
            for i, j in zip(df4, df4.columns)
        ],
        data=df4.to_dict("records"),
        page_size=40,
        sort_action="native",
        filter_action="native",
        export_format="csv",
        style_as_list_view=True,
        )
        return table
    elif "btn-nclicks-2" == ctx.triggered_id:
        return html.Div()



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
def CreateTableFig2right(selectedData):
    if selectedData:
        df_selected_fig2 = parse_callback_json_fig2_right(selectedData, DATABASE)
        table_selected_fig2_right = selected_table(df_selected_fig2)
        return table_selected_fig2_right
    else:
        html.Div()


@app.callback(
    Output("taxonomy_category_output_div","children"),
    Input("filter_dropdown2","value"),
    prevent_initial_call=True,
)
def display_table2(value):
    if value:
        datalist = data_for_taxonomy_category_fig(DATABASE,value)
        df6 = pd.DataFrame(
            data=datalist,
            columns=["genome editing tools", "Taxonomy Category", "the number of genes studied"],
        )
        taxonomy_category_fig = html.Div(
            [
                dcc.Graph(
                    id="Taxonomy_category_figure",
                    figure=px.bar(
                        df6,
                        x="genome editing tools",
                        y="the number of genes studied",
                        color="Taxonomy Category",
                    ),
                ),
            ],
            style={
                "width": "70%",
                # "margin": "1%",
                "display": "inline-block",
                "verticalAlign": "top",
                "textAlign": "right",
            },
        )
        df_taxonomy_cateogry = parse_callback_json_taxonomy_category(value,DATABASE)
        table_filter_dropdown2 = taxonomy_category_selected_table(df_taxonomy_cateogry)
        return taxonomy_category_fig, table_filter_dropdown2
    else:
        html.Div()


@app.callback(
    Output("table_output","children"),
    Input("filter_dropdown","value"),
    prevent_initial_call=True,
)
def display_table(value):
    if value:
        datalist = data_for_species_fig(DATABASE,value)
        df05 = pd.DataFrame(
            data=datalist,
            columns=["genome editing tools", "species", "the number of genes studied"],
        )
        species_fig = html.Div(
            [
                dcc.Graph(
                    id="species_figure",
                    figure=px.bar(
                        df05,
                        x="genome editing tools",
                        y="the number of genes studied",
                        color="species",
                    ),
                ),
            ],
            style={
                "width": "70%",
                # "margin": "1%",
                "display": "inline-block",
                "verticalAlign": "top",
                "textAlign": "right",
            },
        )
        df_species = parse_callback_json_species(value,DATABASE)
        table_filter_dropdown = species_selected_table(df_species)
        return species_fig, table_filter_dropdown
    else:
        html.Div()


@app.callback(
    Output("getools_output_div","children"),
    Input("filter_dropdown_getools","value"),
    prevent_initial_call=True,
)
def display_table_getools(value):
    if value:
        df_getools = parse_callback_json_getools(value,DATABASE)
        table_filter_dropdown_getools = getools_selected_table(df_getools)
        return table_filter_dropdown_getools
    else:
        html.Div()


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8000)
