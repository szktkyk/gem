import dash_mantine_components as dmc
from utils.data_utils import get_filter_values
from utils.schema_utils import VISIBLE_COLUMNS, FILTER_TYPE_DICT
from dash import html



def generate_column_defintions(columns=VISIBLE_COLUMNS):
    data = [
        {
            "field": col,
            # "cellRenderer": RENDERER_TYPE_DICT[col],
            "sortable": False,
            "floatingFilter": True,
            "filter": FILTER_TYPE_DICT[col],
            "tooltipField": col,
            "filterParams": {
                "suppressAndOrCondition": False,
                "buttons": ["reset", "apply"],
                "values": get_filter_values(col)
                if FILTER_TYPE_DICT[col] == "agSetColumnFilter"
                else None,
                # "valueGetter": {
                #     "function": "d3.timeParse('%Y-%m-%d*')(params.data.date)"
                # }
                # if col == "pubdate"
                # else None,
                # "valueFormatter": {"function": "params.data.date"}
                # if col == "pubdate"
                # else None,
            },
        }
        for col in columns
    ]
    # print(data)
    return data


# def generate_column_defs():
#     data = [
#         {"field":"pmid"},
#         {"field":"pubtitle",
#           "cellRenderer": "Test"},

#     ]
#     print(data)
#     return data


def render_columns_modal(
    all_columns=FILTER_TYPE_DICT.keys(),
    visible_columns=VISIBLE_COLUMNS,
):
    return (
        dmc.Container(
            [
                *(
                    dmc.Checkbox(
                        label=col,
                        styles={"labelWrapper": {"color": "#FFD15F"}},
                        checked=True if col in visible_columns else False,
                        id={"type": "checkbox", "field": col},
                    )
                    for col in all_columns
                ),
                dmc.Button(
                    "Apply",
                    id="apply-bttn",
                    style={
                        "border-color": "#FFD15F",
                        "color": "#FFD15F",
                        "margin-bottom": "1em",
                    },
                    variant="outline",
                ),
            ],
            style={
                "width": "300px",
                "margin": "0",
                "border-radius": "0",
            },
        ),
    )
