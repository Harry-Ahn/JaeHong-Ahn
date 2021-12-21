#!/usr/bin/env python
# coding: utf-8

# In[372]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, mpld3
get_ipython().run_line_magic('matplotlib', 'inline')
import json
import datetime
from shapely.geometry import Polygon, mapping
import geopandas as gpd
import folium
from folium.plugins import TimeSliderChoropleth
us_shape = gpd.read_file('USMAP/geo_export_7fe7516b-2db1-4611-9d39-d45cf8d56268.shp')
us_shape = us_shape[['state_name','geometry']]

election = pd.read_csv("1976-2020-president.csv" )

states = set(election['state'])
alaska={}
results = {}
for year in range(1976,2021,4):
    result = {}
    for state in states:      
        state_year = election[(election.year == year) & (election.state == state)]
        dem = max(state_year[state_year.party_simplified == 'DEMOCRAT']['candidatevotes'])
        rep = max(state_year[state_year.party_simplified == 'REPUBLICAN']['candidatevotes'])  
        result[state] = {'dem':dem, 'rep':rep}
        if state == 'ALASKA':
            alaska=result[state]
    results[year] = result

def state_style(state,year,function=False):
    state_results = results[year][state]
    if state_results['rep'] >= (state_results['rep']+state_results['dem'])*0.6:
        color = 'red' 
    elif state_results['rep'] >= (state_results['rep']+state_results['dem'])*0.55:
        color = 'salmon'
    elif state_results['rep'] > (state_results['rep']+state_results['dem'])*0.5: 
        color = 'pink'
    elif state_results['dem'] >= (state_results['rep']+state_results['dem'])*0.6: 
        color = 'Blue'
    elif state_results['dem'] >= (state_results['rep']+state_results['dem'])*0.55: 
        color = 'CornflowerBlue'
    elif state_results['dem'] > (state_results['rep']+state_results['dem'])*0.5: 
        color = 'lightblue'    
    else:
        color = 'White'
  
    if function == False:
        state_style = {
            'opacity': 0,
            'color': color,
        } 
    else:
        state_style = {
             'fillOpacity': 0.5,
             'weight': 1,
             'fillColor': color,
             'color': 'black'}    
  
    return state_style    

def style_function(self):
    state = self['properties']['state_name']
    state = state.upper()
    style = state_style(state,year=2020,function=True)
    return style

usmap = folium.Map(location=[50, -100],zoom_start=3)
choropleth =folium.GeoJson(data= us_shape.to_json(),style_function=style_function)
usmap.add_child(choropleth)


# In[331]:


percent_result={}
for key, value in results[1976].items():
    percent_result[key]=[value['dem']/(value['dem']+value['rep'])*100]
for year in range(1980,2021,4):
    for key, value in results[year].items():
        percent_result[key].append(value['dem']/(value['dem']+value['rep'])*100)

percent=pd.DataFrame(percent_result)
        
NewEngland = percent[['CONNECTICUT', 'MAINE','MASSACHUSETTS','NEW HAMPSHIRE','RHODE ISLAND','VERMONT']]
MidAtlantic = percent[['NEW JERSEY','NEW YORK','PENNSYLVANIA']]
EastNorthCentral=percent[['ILLINOIS','INDIANA','MICHIGAN','OHIO','WISCONSIN']]
WestNorthCentral=percent[['IOWA','KANSAS','MINNESOTA','MISSOURI','NEBRASKA','NORTH DAKOTA','SOUTH DAKOTA']]
SouthAtlantic=percent[['DELAWARE','FLORIDA','GEORGIA','MARYLAND','NORTH CAROLINA','SOUTH CAROLINA',
                       'VIRGINIA','DISTRICT OF COLUMBIA','WEST VIRGINIA']]
EastSouthCentral=percent[['ALABAMA','KENTUCKY','MISSISSIPPI','TENNESSEE']]
WestSouthCentral=percent[['ARKANSAS','LOUISIANA','OKLAHOMA','TEXAS']]
Mountain=percent[['ARIZONA','COLORADO','IDAHO','MONTANA','NEVADA','NEW MEXICO','UTAH','WYOMING']]
Pacific=percent[['ALASKA','CALIFORNIA','HAWAII','OREGON','WASHINGTON']]


# In[332]:


import pandas as pd
import seaborn as sb

sb.heatmap(data=NewEngland.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.title('New England')
plt.show()
plt.title('Mid Atlantic')
sb.heatmap(data=MidAtlantic.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('East North Central')
sb.heatmap(data=EastNorthCentral.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('West North Central')
sb.heatmap(data=WestNorthCentral.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('South Atlantic')
sb.heatmap(data=SouthAtlantic.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('East South Central')
sb.heatmap(data=EastSouthCentral.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('West South Central')
sb.heatmap(data=WestSouthCentral.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('Mountain')
sb.heatmap(data=Mountain.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('Pacific')
sb.heatmap(data=Pacific.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()


# In[282]:


recent = percent.iloc[[8,9,10,11]]
recent_mean=recent.mean()
print(recent_mean)


# In[287]:


p2020=percent.iloc[11]
democrat=[]
republican=[]
for k in percent.keys():
    if k in ['ALASKA','DISTRICT OF COLUMBIA','DELAWARE','MONTANA','NORTH DAKOTA','SOUTH DAKOTA','VERMONT','WYOMING']:
        electoralvotes=3
    elif k in ['HAWAII','MAINE','IDAHO','NEW HAMPSHIRE','RHODE ISLAND']:
        electoralvotes=4
    elif k in ['NEBRASKA','NEW MEXICO','WEST VIRGINIA']:
        electoralvotes=5
    elif k in ['ARKANSAS','IOWA','KANSAS','MISSISSIPPI','NEVADA','UTAH']:
        electoralvotes=6
    elif k in ['CONNECTICUT','OKLAHOMA','OREGON']:
        electoralvotes=7
    elif k in ['KENTUCKY','LOUISIANA']:
        electoralvotes=8
    elif k in ['ALABAMA','COLORADO','SOUTH CAROLINA']:
        electoralvotes=9
    elif k in ['MARYLAND','MINNESOTA','MISSOURI','WISCONSIN']:
        electoralvotes=10
    elif k in ['ARIZONA','MASSACHUSETTS','TENNESSEE']:
        electoralvotes=11
    elif k in ['WASHINGTON']:
        electoralvotes=12
    elif k in ['VIRGINIA']:
        electoralvotes=13
    elif k in ['NEW JERSEY']:
        electoralvotes=14
    elif k in ['NORTH CAROLINA']:
        electoralvotes=15
    elif k in ['GEORGIA','MICHIGAN']:
        electoralvotes=16
    elif k in ['OHIO']:
        electoralvotes=18
    elif k in ['ILLINOIS','PENNSYLVANIA']:
        electoralvotes=20
    elif k in ['FLORIDA','NEW YORK']:
        electoralvotes=29
    elif k in ['TEXAS']:
        electoralvotes=38
    else:
        electoralvotes=55
        
    if p2020[k]>50:
        democrat.append(electoralvotes)
    else:
        republican.append(electoralvotes)
d=sum(democrat)
r=sum(republican)
plt.title(f'2020 Presidential Election Result({d,r})')        
plt.hist(democrat,cumulative=True, label='JOE BIDEN',alpha=0.25,color='b')
plt.hist(republican, cumulative=True, label='DONALD TRUMP',alpha=0.25,color='r')
plt.legend()
plt.show()
        
        
        
        
        


# In[333]:


NewEngland_recent = recent[['CONNECTICUT', 'MAINE','MASSACHUSETTS','NEW HAMPSHIRE','RHODE ISLAND','VERMONT']]
MidAtlantic_recent = recent[['NEW JERSEY','NEW YORK','PENNSYLVANIA']]
EastNorthCentral_recent=recent[['ILLINOIS','INDIANA','MICHIGAN','OHIO','WISCONSIN']]
WestNorthCentral_recent=recent[['IOWA','KANSAS','MINNESOTA','MISSOURI','NEBRASKA','NORTH DAKOTA','SOUTH DAKOTA']]
SouthAtlantic_recent=recent[['DELAWARE','FLORIDA','GEORGIA','MARYLAND','NORTH CAROLINA','SOUTH CAROLINA',
                       'VIRGINIA','DISTRICT OF COLUMBIA','WEST VIRGINIA']]
EastSouthCentral_recent=recent[['ALABAMA','KENTUCKY','MISSISSIPPI','TENNESSEE']]
WestSouthCentral_recent=recent[['ARKANSAS','LOUISIANA','OKLAHOMA','TEXAS']]
Mountain_recent=recent[['ARIZONA','COLORADO','IDAHO','MONTANA','NEVADA','NEW MEXICO','UTAH','WYOMING']]
Pacific_recent=recent[['ALASKA','CALIFORNIA','HAWAII','OREGON','WASHINGTON']]

sb.heatmap(data=NewEngland_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.title('New England - Recent')
plt.show()
plt.title('Mid Atlantic - Recent')
sb.heatmap(data=MidAtlantic_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('East North Central - Recent')
sb.heatmap(data=EastNorthCentral_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('West North Central - Recent')
sb.heatmap(data=WestNorthCentral_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('South Atlantic - Recent')
sb.heatmap(data=SouthAtlantic_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('East South Central - Recent')
sb.heatmap(data=EastSouthCentral_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('West South Central - Recent')
sb.heatmap(data=WestSouthCentral_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('Mountain - Recent')
sb.heatmap(data=Mountain_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()
plt.title('Pacific - Recent')
sb.heatmap(data=Pacific_recent.corr(), annot=True, fmt ='.2f', linewidths=.5, cmap='Blues')
plt.show()


# In[374]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, mpld3
get_ipython().run_line_magic('matplotlib', 'inline')
import json
import datetime
from shapely.geometry import Polygon, mapping
import geopandas as gpd
import folium
from folium.plugins import TimeSliderChoropleth
us_shape = gpd.read_file('US County/geo_export_cf418c13-293c-4eb6-9499-4c250077f044.shp')
us_shape = us_shape[['name','geometry','statefp']]

election = pd.read_csv("countypres_2000-2020.csv" )

counties = set(election['county_name'])

results = {}
for year in range(2020,2021,4):
    result = {}
    for county in counties:
        
        county_year = election[(election.year == year) & (election.county_name == county)]
        if (county_year[county_year.party == 'DEMOCRAT']['candidatevotes']).empty:
            dem = 0
        else:
            dem = max(county_year[county_year.party == 'DEMOCRAT']['candidatevotes'])
        if (county_year[county_year.party == 'REPUBLICAN']['candidatevotes']).empty:    
            rep = 0
        else:
            rep = max(county_year[county_year.party == 'REPUBLICAN']['candidatevotes'])
        
        result[county] = {'dem':dem, 'rep':rep}
        
    results[year] = result
    
def county_style(county,year,function=False):
    if results[year].get(county) is None:
        county_results ={'dem':0,'rep':0}
    else:
        county_results = results[year][county]


    if county_results['rep'] == 0 and county_results['dem']==0:
        color='White'
    elif county_results['rep'] >= (county_results['rep']+county_results['dem'])*0.7:
        color = 'DarkRed' 
    elif county_results['rep'] >= (county_results['rep']+county_results['dem'])*0.6:
        color = 'Red'
    elif county_results['rep'] > (county_results['rep']+county_results['dem'])*0.5: 
        color = 'LightSalmon'
    elif county_results['dem'] >= (county_results['rep']+county_results['dem'])*0.7:
        color = 'DarkBlue'
    elif county_results['dem'] >= (county_results['rep']+county_results['dem'])*0.6:
        color = 'Blue'  
    elif county_results['dem'] > (county_results['rep']+county_results['dem'])*0.5:
        color = 'LightSkyBlue'  

    
    if function == False:
        county_style = {
            'opacity': 0.8,
            'color': color,
        } 
    else:
        county_style = {
             'fillOpacity': 0.8,
             'weight': 0.25,
             'fillColor': color,
             'color': 'black'}     
  
    return county_style    
 
        
def style_function(feature):
    county = feature['properties']['name']
    county = county.upper()
    style = county_style(county,year=2020,function=True)
    return style


countymap = folium.Map(location=[40, -100],zoom_start=4)
choropleth =folium.GeoJson(data= us_shape.to_json(),style_function=style_function)
countymap.add_child(choropleth)


# In[ ]:




