# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:15:49 2020

@author: adam
"""
import os
import serial
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from csv import writer

file_name = 'C:/Users/adam/Desktop/hemp_cannabis.csv'
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')
df = pd.read_csv(file_name)
available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            
            html.Div(id='container-button-timestamp'),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='GrowthRate'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='WaterUse'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'PurpleMarmalade'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Label('Age of Plant'),

    html.Div(dcc.Slider(
        id='crossfilter-day--slider',
        min=df['Day'].min(),
        max=df['Day'].max(),
        value=df['Day'].max(),
        marks={str(Day): str(Day) for Day in df['Day'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
    html.Div([html.Video(src='/static/my-video.webm'),
            html.Button('Start Server', id='btn-nclicks-1', n_clicks=0),
            html.Button('Start Camera', id='btn-nclicks-2', n_clicks=0),
            html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
            html.Label('PlantName,Indicator Name,Day,Value'),
            dcc.Input(id='input-1-state', type='text', value='CsvFile'),
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
            html.Label('-i nameof.file -o nameofnew.file'),
            dcc.Input(id='input-2-state', type='text', value='ndvifile'),
            html.Button(id='submit-button-state2', n_clicks=0, children='Submit'),
            html.Div(id='output-state'),
            html.Div(id='output2-state')],)
])
    


@app.callback(Output('output2-state', 'children'),
              [Input('submit-button-state2', 'n_clicks')],
              [State('input-2-state', 'value')])
def update_output2(n_clicks, input2):
    os.system('python ndvi.py ' + input2)
    return u'''
        The Button has been pressed {} times,
        Input 1 is "{}"
        
    '''.format(n_clicks, input2)
        
@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_output(n_clicks, input1):
    file = open('C:/Users/adam/Desktop/hemp_cannabis.csv','a')
    file.write('\n')
    file.write(input1)

    file.close()
    #append_list_as_row(file_name, input1)
    return u'''
        The Button has been pressed {} times,
        Input 1 is "{}"
        
    '''.format(n_clicks, input1)


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-day--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 day_value):
    dff = df[df['Day'] == day_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['PlantName']
            )

    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['PlantName'])

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='Day', y='Value')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    plant_name = hoverData['points'][0]['customdata']
    dff = df[df['PlantName'] == plant_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(plant_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['PlantName'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


@app.callback(Output('container-button-timestamp', 'children'),
              [Input('btn-nclicks-1', 'n_clicks'),
               Input('btn-nclicks-2', 'n_clicks'),
               Input('btn-nclicks-3', 'n_clicks')])
def displayClick(btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        script_fn = 'C:/Users/adam/.spyder-py3/streamtocomputer.py'
        exec(open(script_fn).read())
        msg = 'Button 1 was most recently clicked'
    elif 'btn-nclicks-2' in changed_id:
        script_fn2 = 'C:/Users/adam/.spyder-py3/streamfrompi.py'
        exec(open(script_fn2).read())
        msg = 'Button 2 was most recently clicked'
    elif 'btn-nclicks-3' in changed_id:
        msg = 'Button 3 was most recently clicked'
    else:
        msg = 'None of the buttons have been clicked yet'
    return html.Div(msg)


def append_list_as_row(file_name, input1):
    # Open file in append mode
    file_name = 'C:/Users/adam/Desktop/hemp_cannabis.csv'
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(input1)

# set up the serial line
def displaySerial():
    ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)
    time.sleep(2)
   
    
    # Read and record the data
    data =[]                       # empty list to store the data
    for i in range(50):
        
        b = ser.readline() 
       # ser.open()
       # ser.isOpen()        # read a byte string
        string_n = b.decode()  # decode byte string into Unicode  
        string = string_n.rstrip() # remove \n and \r
        words = string.split()
        intimade = words[1].translate('!:@#$')
        dict(map(str.strip, line.split(':', 1)) for line in intimade.splitlines())
        flt = float(intimade[3])        # convert string to float
        #print(flt)
        data.append(string)           # add to the end of data list
        time.sleep(0.1)            # wait (sleep) 0.1 seconds
        
    
    for line in data:
        return line
    
    
    



if __name__ == '__main__':
    app.run_server(debug=True)
