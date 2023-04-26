

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc






# In[24]:


# dashboard where you can show student attendance, single ticket purchases or both
# References Used: https://dash.plotly.com/dash-enterprise?_gl=1*16cti19*_ga*MjA4NjQ5MjI2OC4xNjY2MjkwMjIx*_ga_6G7EE0JNSC*MTY4MTgyNzQxNS4yNi4wLjE2ODE4Mjc0MTUuMC4wLjA.
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
# https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/#sourceCode




# Build App
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

server = app.server

# Game student data
student_df = pd.read_excel('BB - Student Data.xlsx')
# Get rid of NaN
student_df = student_df.dropna()


# In[3]:


# Change column names
student_df = student_df.rename(columns={'Season Code':'Season', 'Item Full Name':'Opponent'})

# Change `Year` column to show full year
student_df.Season = student_df.Season.replace(regex=['BB'],value='20')



# In[4]:


# Opponent column

# Get rid of anything that says `Baseball` - it's a given
student_df = student_df.replace(regex=['Baseball', 'Basedball '],value='')

# Try new DayofWeek col by string splitting on parentheses
student_df[['Opponent', 'DoW']] = student_df['Opponent'].str.split("(", n = 1, expand = True)

# Split again - make a new DoW column (will merge the two later)
student_df[['Opponent', 'DayofWeek']] = student_df['Opponent'].str.split("-", n = 1, expand = True)
# Get rid of random leading and trailing spaces
student_df['Opponent'] = student_df['Opponent'].str.strip()

# Combine DoW and DayofWeek columns
student_df['DOW'] = student_df['DoW'].astype(str) + student_df['DayofWeek'].astype(str)

# Get rid of `None` from duplicate columns
student_df.DOW = student_df.DOW.replace(regex=['None'],value='')

# Get rid of trailing parentheses
student_df.DOW = student_df.DOW.replace(regex=['\) ', '\)'],value='')

# Missing values
student_df.DOW = student_df.DOW.replace(regex=[''],value='None')

# New column for original date
student_df[['DOW', 'OriginalDoW']] = student_df['DOW'].str.split("- ", n = 1, expand = True)

# Get rid of extra stuff
student_df.OriginalDoW = student_df.OriginalDoW.replace(regex=['Originally ', 'GAME 1 FRIDAY', 'GAME 1', 'GAME 2'],value='')
student_df.OriginalDoW = student_df.OriginalDoW.replace(regex=['', np.nan],value='None')

# Get rid of GAME X information - can be inferred when looking at the data  based on opponent
student_df.DOW = student_df.DOW.replace(regex=[' GAME 2', '  GAME 1', ' Game 1', ' Game #2 Saturday', ' \(Game 2 Friday 4-21', ' GAME 2-FRIDAY', ' \(Game 2DH', ' GAME 2 on Sunday', ' GAME 1', ' \(GAME 2',  ' \(GAME 1', 'GAME 1', '- Originally Tuesday', ' on Sunday', ' - FRIDAY', '-FRIDAY', ' - ', ' -', ' '],value='')

# Change vartype
student_df.Attendance = student_df.Attendance.astype(int)

# Get rid of funky index
student_df = student_df.reset_index()

# Get rid of old Days of Week columns
student_df = student_df.drop(columns=['DoW', 'DayofWeek', 'index'])

# Unique game ID column
student_df['Game_ID'] = range(len(student_df))
student_df['Game_ID'] += 1

# Rename for my sanity
student_df = student_df.rename(columns={'DOW': 'Day of Week', 'OriginalDoW':'Original Day of Week'})



# Game Data 2022

# In[5]:


# read in excel sheet to dataframe

game22_data = pd.read_excel('BB - Game Data.xlsx', sheet_name="2022")

# drop Season Code column and rename Item Full Name
game22_data = game22_data.rename(columns={'Item Full Name':'Opponent'}).drop(columns=['Season Code'])

# as done with student data, separate DoW from opponent 
game22_data = game22_data.replace(regex=['Baseball', 'Basedball '],value='')
game22_data[['Opponent', 'Day of Week']] = game22_data['Opponent'].str.split("(", n = 1, expand = True)
game22_data = game22_data.drop(columns=['Day of Week'])
game22_data['Day of Week'] = game22_data.Date.dt.day_name()


# In[6]:


# Change to int
student_df['Season'] = student_df['Season'].astype(int)

# join with student attendance dataframe to get student attendance numbers per game
student_attendance22 = game22_data.merge(student_df[student_df['Season']==2022], 
                                         how="left", on='Item Code').drop(
                                             columns=['Season','Day of Week_y','Opponent_y','Original Day of Week']).rename(
                                                 columns={"Opponent_x":"Opponent", "Day of Week_x":"Day of Week"}
                                             )

## Game Data 2019

# read in excel sheet to dataframe

game19_data = pd.read_excel('BB - Game Data.xlsx', sheet_name="2019")

# drop Season Code column and rename Item Full Name
game19_data = game19_data.rename(columns={'Item Full Name':'Opponent'}).drop(columns=['Season Code'])

# as done with student data, separate DoW from opponent 
game19_data = game19_data.replace(regex=['Baseball', 'Basedball '],value='')
game19_data[['Opponent', 'Day of Week']] = game19_data['Opponent'].str.split("(", n = 1, expand = True)
game19_data = game19_data.drop(columns=['Day of Week'])
game19_data['Day of Week'] = game19_data.Date.dt.day_name()
# join with student attendance dataframe to get student attendance numbers per game
student_attendance19 = game19_data.merge(student_df[student_df['Season']==2019], 
                                         how="left", on='Item Code').drop(
                                             columns=['Season','Day of Week_y','Opponent_y','Original Day of Week']).rename(
                                                 columns={"Opponent_x":"Opponent", "Day of Week_x":"Day of Week"}
                                             )

## Game Data 2018

# read in excel sheet to dataframe

game18_data = pd.read_excel('BB - Game Data.xlsx', sheet_name="2018")

# drop Season Code column and rename Item Full Name
game18_data = game18_data.rename(columns={'Item Full Name':'Opponent'}).drop(columns=['Season Code'])

# as done with student data, separate DoW from opponent 
game18_data = game18_data.replace(regex=['Baseball', 'Basedball '],value='')
game18_data[['Opponent', 'Day of Week']] = game18_data['Opponent'].str.split("(", n = 1, expand = True)
game18_data = game18_data.drop(columns=['Day of Week'])
game18_data['Day of Week'] = game18_data.Date.dt.day_name()


# join with student attendance dataframe to get student attendance numbers per game
student_attendance18 = game18_data.merge(student_df[student_df['Season']==2018], 
                                         how="left", on='Item Code').drop(
                                             columns=['Season','Day of Week_y','Opponent_y','Original Day of Week']).rename(
                                                 columns={"Opponent_x":"Opponent", "Day of Week_x":"Day of Week"}
                                             )


# # Dashboard





# JupyterDash example code found at https://medium.com/plotly/introducing-jupyterdash-811f1f57c02e

# load libraries

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# In[10]:


# get single game ticket revenue data for 2022
revenue_dict2022 = pd.read_excel('2022 Single Game Ticket Revenue.xlsx', sheet_name=['2022'])
revenue_df2022 = revenue_dict2022.get('2022')

# Join single game revenue data with game data and group by game ID
game_attendance22 = list(revenue_df2022.groupby('Item Code').count()['Order Qty (Total)'])

# remove row where Item Code equals BB35, this was a canceled game
revenue_df2022 = revenue_df2022[revenue_df2022['Item Code'] != 'BB35']
revenue_df2022['Sale Type'] = np.where(revenue_df2022['Account Name'].str.contains("GATE SALES"), 'Gate Sale', 
                        'Pre-Sale')

# create dataframe with all ticket sales joined with game data for 2022
ticket_sales22 = revenue_df2022.groupby(['Item Code','Sale Type']).agg({"Order Qty (Total)":"count"}).reset_index()
ticket_sales22 = ticket_sales22.merge(game22_data, how="left", on="Item Code").rename(columns={'Order Qty (Total)':'Sales'})

# create ticket sales df for 2019

revenue_dict2019 = pd.read_excel('2022 Single Game Ticket Revenue.xlsx', sheet_name=['2019'])
revenue_df2019 = revenue_dict2019.get('2019')

revenue_df2019['Sale Type'] = np.where(revenue_df2019['Account Name'].str.contains("GATE SALES"), 'Gate Sale', 
                        'Pre-Sale')

# create dataframe with all ticket sales joined with game data for 2022
ticket_sales19 = revenue_df2019.groupby(['Item Code','Sale Type']).agg({"Order Qty (Total)":"count"}).reset_index()
ticket_sales19 = ticket_sales19.merge(game19_data, how="left", on="Item Code").rename(columns={'Order Qty (Total)':'Sales'})

# create ticket sales df for 2018

revenue_dict2018 = pd.read_excel('2022 Single Game Ticket Revenue.xlsx', sheet_name=['2018'])
revenue_df2018 = revenue_dict2018.get('2018')

revenue_df2018['Sale Type'] = np.where(revenue_df2018['Account Name'].str.contains("GATE SALES"), 'Gate Sale', 
                        'Pre-Sale')

# create dataframe with all ticket sales joined with game data for 2022
ticket_sales18 = revenue_df2018.groupby(['Item Code','Sale Type']).agg({"Order Qty (Total)":"count"}).reset_index()
ticket_sales18 = ticket_sales18.merge(game18_data, how="left", on="Item Code").rename(columns={'Order Qty (Total)':'Sales'})


# In[13]:



# create dataframe that holds gate sale counts for each game in 2022
gate_sales22 = revenue_df2022[revenue_df2022['Account Name'].str.contains("GATE SALES")]
gate_sales22 = gate_sales22.groupby('Item Code').count().loc[:,'Order Qty (Total)'].to_frame()
gate_sales22 = game22_data.merge(gate_sales22, how="left", on="Item Code").rename(columns={'Order Qty (Total)':'Sales'})


# In[15]:


# create dataframe that holds pre sale purchase counts for each game in 2022
pre_sales22 = revenue_df2022[revenue_df2022['Account Name'].str.contains("GATE SALES")==False]
pre_sales22 = pre_sales22.groupby('Item Code').count().loc[:,'Order Qty (Total)'].to_frame()
pre_sales22 = game22_data.merge(pre_sales22, how="left", on="Item Code").rename(columns={'Order Qty (Total)':'Sales'})


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 85,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    #"padding": "2rem 1rem",
}


ticket_sidebar = html.Div(
    [
        html.H5("UVA Baseball Ticket Sales", className="display-4", style={"font-size":"20px", "color":"#232D48"}),
        html.Hr(),
          html.Div(children=[
                html.Label(["Select Year: ",
              dcc.RadioItems(['2018', '2019','2022'], '2022', id='year_button_ticket'),],),
              html.Br(),
              html.Label(["Select Factor: ",
                dcc.Dropdown(
                  ['Weather Condition','Opponent','Conference Game','UVA Rank','Opp Rank','Major Promo', 'Day of Week','Temperature'],
                  id='factor_dropdown_ticket',
                  value='Day of Week')
              ], style={'width': '85%'}),
               ],),
    ],
    style=SIDEBAR_STYLE,
)

student_sidebar = html.Div(
    [
        html.H5("UVA Student Attendance", className="display-4", style={"font-size":"20px", "color":"#232D48"}),
        html.Hr(),
           html.Div(children=[
            html.Label(["Select Year: ",
              dcc.RadioItems(['2018', '2019','2022'], '2022', id='year_button_student'),],),
            html.Br(),
            html.Label(["Select Factor: ",
                dcc.Dropdown(
                  ['Weather Condition','Opponent','Conference Game','UVA Rank','Opp Rank','Major Promo', 'Day of Week', 'Temperature'],
                  id='factor_dropdown_student',
                  value='Day of Week')
            ],style={"width":"85%"}),
          ],
        ),
    ],
    style=SIDEBAR_STYLE,
)

ticket_content = html.Div(children=[
                  dcc.Graph(id="ticket_graph"),
                ], style=CONTENT_STYLE)

student_content = html.Div(children=[
                dcc.Graph(id="student_graph")
                ], style=CONTENT_STYLE)


app.layout = html.Div([
    dcc.Tabs([
      dcc.Tab(label="Ticket Sales", children=[
        html.Div(children=[
            ticket_sidebar,
            ticket_content,
        ]),
          
      ]),
      dcc.Tab(label="Student Attendance", children=[
        html.Div(children=[
        student_sidebar,
        student_content,
      ],),
    ]),
  ]),
])

# Define callback to update ticket sales graph
@app.callback(
   Output('ticket_graph', 'figure'),
    [Input('factor_dropdown_ticket',"value"),
     Input('year_button_ticket','value'),],
)
def update_ticket_figure(factor_dropdown_ticket, year_button_ticket):
  if(year_button_ticket == '2022'):
    df = ticket_sales22
  elif(year_button_ticket == '2019'):
    df = ticket_sales19
  else:
    df = ticket_sales18
  if(factor_dropdown_ticket=="Temperature"):
    fig1 = px.scatter(df, x=factor_dropdown_ticket, y='Sales', facet_col="Sale Type", facet_col_spacing=0.06,
           hover_data=['Opponent', 'Promo Type'], color='Item Code', color_discrete_sequence = ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9c74F', '#90BE6D','#43AA8B','#4D908E', '#577590','#277DA1'])
    # below code found at: https://stackoverflow.com/questions/60997189/how-can-i-make-faceted-plots-in-plotly-have-their-own-individual-yaxes-tick-labe
    fig1.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig1.update_layout(showlegend=False, yaxis_title="Total Season Sales", plot_bgcolor="white")
    fig1.update_xaxes(linecolor="black")
    fig1.update_yaxes(linecolor="black", gridcolor="black")
  else:
    fig1 = px.bar(df, x=factor_dropdown_ticket, y='Sales', facet_col="Sale Type", facet_col_spacing=0.06,
           hover_data=['Opponent', 'Promo Type'],color = 'Item Code', color_discrete_sequence = ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9c74F', '#90BE6D','#43AA8B','#4D908E', '#577590','#277DA1'])
    fig1.update_yaxes(matches=None, linecolor="black", gridcolor="black")
    fig1.update_xaxes(type="category", linecolor="black")
    fig1.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig1.update_layout(showlegend=False, yaxis_title="Total Season Sales", plot_bgcolor="white")
    if(factor_dropdown_ticket=="Opponent"):
      fig1.update_xaxes(tickangle=45)

  return fig1

   
@app.callback(
    Output('student_graph','figure'),
    [Input("factor_dropdown_student",'value'),
    Input("year_button_student","value"),],
) 
def update_student_figure(factor_dropdown_student, year_button_student):
  if(year_button_student == '2022'):
    stu_df = student_attendance22
  elif(year_button_student == '2019'):
    stu_df = student_attendance19
  else:
    stu_df = student_attendance18
  if(factor_dropdown_student=='Temperature'):
    fig2 = px.scatter(stu_df, x=factor_dropdown_student, y='Attendance',
          hover_data=['Opponent', 'Promo Type'], color='Item Code',  color_discrete_sequence = ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9c74F', '#90BE6D','#43AA8B','#4D908E', '#577590','#277DA1']) 
    fig2.update_layout(showlegend=False, yaxis_title="Total Season Attendance", plot_bgcolor="white")
    fig2.update_xaxes(linecolor="black")
    fig2.update_yaxes(linecolor="black", gridcolor="black")
  else:
    fig2 = px.bar(stu_df, x=factor_dropdown_student, y='Attendance', 
          hover_data=['Opponent', 'Promo Type'], color='Item Code',  color_discrete_sequence = ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9c74F', '#90BE6D','#43AA8B','#4D908E', '#577590','#277DA1'])
    fig2.update_layout(showlegend=False, yaxis_title="Total Season Attendance", plot_bgcolor="white")
    fig2.update_yaxes(linecolor="black", gridcolor="black")
    fig2.update_xaxes(type="category", linecolor="black")
    if(factor_dropdown_student=="Opponent"):
      fig2.update_xaxes(tickangle=45)

 
  return fig2





# Run app and display result inline in the notebook
if __name__ == '__main__':
  app.run_server(host="0.0.0.0", port="8050")






