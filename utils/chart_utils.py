# TODO: グラフ用のコードを書く
import plotly.graph_objects as go
from plotly import express as px
import config
import polars as pl

def fig1_and_fig2(df):
    x_labels = ["TALEN", "ZFN", "Base editor", "Prime editor", "CRISPR-Cas3", "CRISPR-Cas12", "CRISPR-Cas13", "CRISPRi", "CRISPRa"]
    df = df.filter(pl.col('taxonomy_category').is_not_null())
    data = []
    for tool in x_labels:
        for taxonomy in df['taxonomy_category'].unique().to_list():
            # 'taxonomy_category'がtaxonomyである行を抽出
            df_taxonomy = df.filter(pl.col('taxonomy_category') == taxonomy)
            # 'getool'にtoolが含まれる行数をカウント
            df_tool = df_taxonomy.filter(pl.col('getool').str.contains(tool))
            # uniqueなpmidの数をカウント
            count_pmid = df_tool["pmid"].n_unique()
            count_gene = df_tool["genesymbol"].n_unique()
            data.append({"genome editing tool": tool, "taxonomy category": taxonomy, "publication count": count_pmid, "gene count": count_gene})

    df_fig = pl.DataFrame(data)
    fig1 = px.bar(df_fig, x="genome editing tool", y="publication count", color="taxonomy category", title = "Publication Count")
    fig2 = px.bar(df_fig, x="genome editing tool", y="gene count", color="taxonomy category", title = "Gene Count")
    return fig1, fig2



def fig3_and_fig4(df):
    df = df.filter(pl.col('taxonomy_category').is_not_null())
    x_labels = ["CRISPR-Cas9","TALEN", "ZFN", "Base editor", "Prime editor", "CRISPR-Cas3", "CRISPR-Cas12", "CRISPR-Cas13", "CRISPRi", "CRISPRa"]
    data_fig3 = []
    data_fig4 = []
    for i in range(2009,2025):
        df_year = df.filter(pl.col('pubdate').str.contains(i))
        for tool in x_labels:
            # df_taxonomyの'getool'にtoolが含まれる行を抽出
            df_getool = df_year.filter(pl.col('getool').str.contains(tool))
            count_getool = df_getool["pmid"].n_unique()
            data_fig3.append({"genome editing tool": tool, "year": i, "publication count": count_getool})
        for taxonomy in df['taxonomy_category'].unique().to_list():
            df_taxonomy = df_year.filter(pl.col('taxonomy_category') == taxonomy)
            count_taxonomy = df_taxonomy["pmid"].n_unique()
            data_fig4.append({"taxonomy category": taxonomy, "year": i, "publication count": count_taxonomy})
    
    df_fig3 = pl.DataFrame(data_fig3)
    df_fig4 = pl.DataFrame(data_fig4)
    fig3 = px.bar(df_fig3, x="year", y="publication count", color="genome editing tool", title = "Publication Count by year (genome editing tool)")
    fig4 = px.bar(df_fig4, x="year", y="publication count", color="taxonomy category", title = "Publication Count by year (taxonomy category)")
    return fig3, fig4
            


#     for tool in x_labels:
#         for i in range(2009, 2025):
#             df_year = df.filter(pl.col('pubdate').str.contains(i))
#             # df_taxonomyの'getool'にtoolが含まれる行を抽出
#             df_getool = df_year.filter(pl.col('getool').str.contains(tool))
#             count = df_getool["pmid"].n_unique()
#             fig3_count.append({"genome editing tool": tool, "year": i, "publication count": count})

#     df_fig2 = pl.DataFrame(fig3_count)

#     fig2 = px.bar(df_fig2, x="year", y="publication count", color="genome editing tool", title = "Publication Count by year")
#     # fig2.show()
#     return fig2

# def fig4(df):
#     df = df.filter(pl.col('taxonomy_category').is_not_null())
#     fig4_count = []
#     for taxonomy in df['taxonomy_category'].unique().to_list():
#         for i in range(2009, 2025):
#             df_year = df.filter(pl.col('pubdate').str.contains(i))
#             df_getool = df_year.filter(pl.col('taxonomy_category') == taxonomy)
#             count = df_getool["pmid"].n_unique()
#             fig4_count.append({"taxonomy category": taxonomy, "year": i, "publication count": count})

#     df_fig2 = pl.DataFrame(fig4_count)

#     fig4 = px.bar(df_fig2, x="year", y="publication count", color="taxonomy category", title = "Publication Count by Species category")
#     # fig2.show()
#     return fig4







