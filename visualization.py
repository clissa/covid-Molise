#  Copyright (c) 2021. Luca Clissa
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from utils import is_business_day

color_dict = {
    'Reali': 'peru', 'Previsioni': 'rgb(31, 119, 180)', 'Upper Bound': 'rgba(0,100,80,0.2)',
    'Lower Bound': 'rgba(0,100,80,0.2)'
}


def make_table(df, real_col):
    import plotly.graph_objs as go

    headerColor = 'lightskyblue'
    rowEvenColor = 'aliceblue'
    rowOddColor = 'white'
    font_family = 'Cambria Math'
    line_color = 'darkslategray'
    header_color = 'snow'
    text_color = 'dimgray'

    view = df.copy()
    view.columns = [real_col.replace("_", " ").title(), "Previsioni", "Lower C.I. 95%", "Upper C.I. 95%"]
    out_cols = ["Data"]
    out_cols.extend(view.columns)
    out_cols = [f"<b>{col}</b>" for col in out_cols]
    view = view.round(2)

    return (
        go.Table(
            header=dict(
                values=out_cols,
                line_color=line_color,
                fill_color=headerColor,
                align=['left', 'center'],
                font=dict(color=header_color, size=18, family=font_family)
            ),
            cells=dict(
                values=[view.index.date, view[real_col.replace("_", " ").title()], view["Previsioni"],
                        view["Lower C.I. 95%"], view["Upper C.I. 95%"]],
                line_color=line_color,
                # 2-D list of colors for alternating rows
                fill_color=[[rowOddColor, rowEvenColor] * round(view.shape[0])],
                align=['left', 'center'],
                font=dict(color=text_color, size=16, family=font_family)
            ))
    )


def draw_scatter(df, col, label, marker_symbols, marker_sizes):
    import plotly.graph_objs as go

    return (
        go.Scatter(
            name=label,
            x=df.index,
            y=df[col],
            mode='markers+lines',
            line=dict(color=color_dict[label]),
            marker=dict(symbol=marker_symbols, size=marker_sizes),
        )
    )


def draw_confidence_bands(df, col, label, fillcolor='rgba(0,100,80,0.2)', marker_col="#444"):
    import plotly.graph_objs as go

    return (
        go.Scatter(
            name=label,
            x=df.index,
            y=df[col],
            mode='lines',
            marker=dict(color=marker_col),
            fillcolor=fillcolor,
            line=dict(width=0),
            fill='tonexty',
            showlegend=False
        )
    )


def plot_pred(pred_df, real_df, real_col, pred_col="fitted", upper_col="upper", lower_col="lower", outpath=None,
              show=True):
    import datetime
    from pathlib import Path
    from plotly.subplots import make_subplots

    # compute last date of training data
    last_date = pred_df.index[0]
    last_date -= datetime.timedelta(days=1)
    y_annotation = pred_df[upper_col].max()
    min_y_plot = real_df[-21:][real_col].min()
    max_y_plot = real_df[-21:][real_col].max()

    symbol_business = 'circle'
    symbol_holidays = 'diamond'
    sz_business = 7
    sz_holidays = 10
    marker_symbols_real = [symbol_business if is_business_day(d.date()) else symbol_holidays for d in real_df.index]
    marker_sizes_real = [sz_business if is_business_day(d.date()) else sz_holidays for d in real_df.index]
    marker_symbols_pred = [symbol_business if is_business_day(d.date()) else symbol_holidays for d in pred_df.index]
    marker_sizes_pred = [sz_business if is_business_day(d.date()) else sz_holidays for d in pred_df.index]

    fig = make_subplots(
        rows=2, cols=1,
        #     shared_xaxes=True,
        vertical_spacing=0.2,
        specs=[[{"type": "scatter"}],
               [{"type": "table"}]]
    )

    fig.add_trace(draw_scatter(real_df, real_col, 'Reali', marker_symbols_real, marker_sizes_real), row=1, col=1)
    fig.add_trace(draw_scatter(pred_df, pred_col, 'Previsioni', marker_symbols_pred, marker_sizes_pred), row=1, col=1)
    fig.add_trace(draw_confidence_bands(pred_df, upper_col, 'Upper Bound'), row=1, col=1)
    fig.add_trace(draw_confidence_bands(pred_df, lower_col, 'Lower Bound'), row=1, col=1)

    fig.add_shape(type="line",
                  x0=last_date, y0=0, x1=last_date, y1=y_annotation,
                  name="Ultimi dati training",
                  line=dict(
                      color="firebrick",
                      width=4,
                      dash="dashdot",
                  )
                  ),
    fig.add_annotation(x=last_date, y=min_y_plot,
                       ax=-50,
                       ay=20,
                       xanchor="right",
                       yanchor="top",
                       text=f"Ultimi dati training:\n{last_date.date()}",
                       showarrow=True,
                       arrowhead=2),
    fig.update_layout(
        xaxis_title='Data',
        xaxis=dict(range=[last_date - datetime.timedelta(14), last_date + datetime.timedelta(8)], autorange=False),
        yaxis_title='N. ospedalizzazioni',
        yaxis=dict(range=[min_y_plot - y_annotation / 10, max_y_plot + y_annotation / 10], autorange=False),
        title=f'Andamento {real_col}'.title(),

        hovermode="x",
        font=dict(
            family="Courier New, monospace",
            size=16,
        )
    )

    fig.add_trace(make_table(pred_df, real_col), row=2, col=1)

    fig.update_layout(width=1000, height=800,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    if show:
        fig.show()
    else:
        if not outpath:
            outpath = f"./results/{last_date.date()}/{real_col}.html"
        Path(outpath).parent.mkdir(exist_ok=True, parents=True)
        fig.write_html(outpath)
        fig.write_image(outpath.replace(".html", ".png"))
    return fig
