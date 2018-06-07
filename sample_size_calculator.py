import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import flask
from flask_cors import CORS
import os

import sys
sys.path.append('code/')
from wrapper import *

app = dash.Dash('Sample_size_calculator')
server = app.server

app.layout = html.Div([
    html.H2('Sample Size Calculator',style ={'textAlign':'center'}),
    html.H5('Created by Sri Santhosh Hari, Sooraj Subrahmannian and Devesh Maheshwari',style ={'textAlign':'center'}),

    # Row 2: Hover Panel and Graph
    html.Div([
        html.Div([
            
            html.Br(),
            
            html.Div(html.B('Type of Test'),style=dict( maxHeight='200px', fontSize='15px' )),
            dcc.RadioItems(
                id = 'test_type',
                options=[
                    {'label': 'Comparison of Means', 'value': 'mean'},
                    {'label': 'Comparison of Proportions', 'value': 'prop'}],
                value='mean'),

            html.Br(),
            
            html.Div(html.B('One tailed or Two tailed'),style=dict( maxHeight='200px', fontSize='15px' )),
            dcc.RadioItems(
                id = 'tail_select',
                options=[
                    {'label': 'One tailed', 'value': 'one'},
                    {'label': 'Two tailed', 'value': 'two'}],
                value='two'),

            html.Br(),
            html.Div(html.B('Significance Level (α)'),style=dict( maxHeight='200px', fontSize='15px' )),
            dcc.RangeSlider(
                id='significance',
                min=0.01,
                max=0.1,
                marks={np.round(i,2):np.round(i,2) for i in np.arange(0.01,0.1,0.01)},
                step=0.01,
                value=[0.05, 0.1]),

            html.Br(),
            html.Div(html.B('Power (1-β)'),style=dict( maxHeight='200px', fontSize='15px' )),
            dcc.RangeSlider(
                id='power',
                min=0.75,
                max=1,
                marks={np.round(i,2):np.round(i,2) for i in np.arange(0.75,1,0.05)},
                step=0.05,
                value=[0.8, 0.8]),
            html.Br(),
            
            html.B(html.Div(id = 'nme_slider',
                     children ='Effect Size (δ)',
                     style=dict( maxHeight='200px', fontSize='15px' ))),
            dcc.RangeSlider(
                id='effect_size',
                min=0,
                max=3,
                marks={np.round(i,1):np.round(i,1) for i in np.arange(0,3,0.3)},                
                step=0.3,
                value=[0.5, 0.5]),
                        html.Br(),
            
            html.B(html.Div(id = 'k_slider',
                     children ='k (n1/n2)',
                     style=dict( maxHeight='200px', fontSize='15px' ))),
            dcc.Slider(
                id='k',
                min=0.1,
                max=2,
                marks={np.round(i,1):np.round(i,1) if index%2==0 else '' for index,i in enumerate(np.arange(0.1,2,0.1)) },
                step=0.1,
                value=1),
        ], className='three columns', style=dict(height='300px')),
            

        html.Div([
            dcc.Graph(id='clickable-graph',
                      style=dict(width='700px',height='550px'),
                      hoverData=dict(points=[dict(pointNumber=0)] )),
        
        html.B(html.Div(id = 'warning',
                     children ='',
                     style=dict( maxHeight='200px', fontSize='15px',color='red'))),

        ], className='nine columns', style=dict(textAlign='center')),
    ], className='row' ),
    

 ], className='container')

@app.callback(
    Output('clickable-graph', 'figure'),
    [Input('test_type', 'value'), 
     Input('tail_select', 'value'),
     Input('significance', 'value'),
     Input('power', 'value'),
     Input('effect_size', 'value'),
     Input('k', 'value')
    ])
def wrap_function_call(tt,tail,alpha,power,effect_size,k):
    try :
        return wrap_calculations(test_type=tt,
                             tailed=tail,
                             alpha=alpha,
                             power=power,
                             effect_size=effect_size,
                             k=k)
    except:
        return None


@app.callback(
    Output('nme_slider', 'children'),
    [Input('test_type', 'value')])
def title_change(value):
    return 'Effect Size (δ)' if value == 'mean' else 'Left slider is π1 and Right slider is π2'

@app.callback(
    Output('warning', 'children'),
    [Input('test_type', 'value'), 
     Input('tail_select', 'value'),
     Input('significance', 'value'),
     Input('power', 'value'),
     Input('effect_size', 'value'),
     Input('k', 'value')
    ])
def wrap_function_call(tt,tail,alpha,power,effect_size,k):
    
    f = None
    try :
        wrap_calculations(test_type=tt,
                             tailed=tail,
                             alpha=alpha,
                             power=power,
                             effect_size=effect_size,
                             k=k)
    except Exception as e:
        print(e)
        f =str(e)
    return f



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]


for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(port=8052,debug=True,host='0.0.0.0')
