#from pivottablejs import pivot_ui

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_pivottable
from django_plotly_dash import DjangoDash

#app = dash.Dash(__name__)
app = DjangoDash('efiga_pivot_app')

#app.scripts.config.serve_locally = True
#app.css.config.serve_locally = True

from py2neo import Graph
import pandas as pd
graph = Graph("bolt://localhost:7687", auth=("neo4j", "test"))
cursor = graph.run("MATCH (a:EfigaRecord) RETURN a")
rs = []
for record in cursor: rs.append(dict(record.values(0)[0]))
	
df = pd.DataFrame(rs)

#pivot_ui(df,outfile_path="pivottablejs.html")

app.title = 'Efiga Data'
app.layout = html.Div([
    dash_pivottable.PivotTable(
        id='table',
        data=df.to_dict('records'),
        cols=[],
        colOrder="key_a_to_z",
        rows=[],
        rowOrder="key_a_to_z",
        rendererName="Table",
        aggregatorName="Count",
        vals=[],
        valueFilter={}
    ),
    dcc.Markdown(
        id='output'
    ),
    dcc.Markdown(
        id='output'
    )
])


@app.callback(Output('output', 'children'),
              [Input('table', 'cols'),
               Input('table', 'rows'),
               Input('table', 'rowOrder'),
               Input('table', 'colOrder'),
               Input('table', 'aggregatorName'),
               Input('table', 'rendererName')])
               
def display_props(cols, rows, row_order, col_order, aggregator, renderer):
    return """
        Columns: {}
        
        rows: {}
        
        rowOrder: {}
        
        colOrder: {}
        
        aggregatorName: {}
        
        rendererName: {}
    """.format(str(cols), str(rows), row_order, col_order, aggregator, renderer)


if __name__ == '__main__':
    app.run_server(debug=True)
