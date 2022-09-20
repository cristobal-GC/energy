# -*- coding: utf-8 -*-
"""
This script generates a plot showing LNG send-out capacities in EU countries

@author: cristobal-GC
"""


import pandas as pd
import matplotlib.pyplot as plt



#################### Analysis parameters

### Winter consumption (from 1/Nov to 31/March) is assumed to be 55% of year consumption
# Ref: EUROSTAT
# https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gasm/default/table?lang=en
winter_cons_factor = 0.55
winter_days = 151




#################### Plot parameters

### font sizes
tamano = 18
tamano_small = 16

params = {'axes.labelsize': tamano,
          'xtick.labelsize': tamano,
          'ytick.labelsize': tamano}     

plt.rcParams.update(params)


### Colours
color_bar = (.3,0.5,0.)



### Define figure and axes size
figure_width = 30 # cm
figure_height = 20 # cm

left_margin = 3 # cm
right_margin = .5 #cm
top_margin = .2 # cm
bottom_margin = 5.6 # cm






#################### Data processing

### Read data
data = pd.read_csv('data/LNG_EU.csv',delimiter=';',skiprows=1)

# Columns description:
#	'LNG Inventory (1000 m3)'	: Stored LNG in tanks on gas day 2022-09-18
#	'Send-out (GWh/d)'		: Emission on gas day 2022-09-18
#	'DTMI (1000 m3)'		: "Declared total maximum inventory", storage capacity in LNG tanks
#	'DTRS (GWh/d)'			: "Declared total reference send-out", emission capacity into the gas system


# Remove EU row
df1 = data[data["Name"]!="EU"]

# Sort by emission capacity DTRS (GWh/d)
df = df1.sort_values("DTRS (GWh/d)",ascending=False)

# Select EU row
dfEU = data[data["Name"]=="EU"]



#################### Make plot

### Create fig and ax
left    = left_margin / figure_width # Percentage from width
right   = right_margin / figure_width # Percentage from width
top     = top_margin / figure_height # Percentage from height
bottom  = bottom_margin / figure_height # Percentage from height

width  = 1 - left - right
height = 1 - top - bottom

cm2inch = 1/2.54 # inch per cm

fig = plt.figure(figsize=(figure_width*cm2inch,figure_height*cm2inch))
ax = fig.add_axes((left, bottom, width, height))



### Add bars
df.plot(x='Name', y="DTRS (GWh/d)",
        color=color_bar,
        kind='bar',width=.9,
        legend=None,
        ax=ax)
            


#################### Message 1


EU_LNG_capacity = dfEU.loc[0,['DTRS (GWh/d)']].item()
ax.text(2, 1900, f'EU send-out capacity from LNG to gas system: {round(EU_LNG_capacity/10)/100} TWh/d', fontsize=tamano)

# Consumption in 1 winter day
#EU_year_cons = max(dfEU.loc[0,['Consumption (TWh)']].item(),4151.8)
#cons_1winter_day = EU_year_cons*winter_cons_factor/winter_days
# Winter days covered given current storage and considering minimum storage level
#stored_EU = dfEU.loc[0,['Gas in storage (TWh)']].item()
#winter_days_covered = round((stored_EU*(1-min_storage_level))/cons_1winter_day)
#ax.text(5, 220, f'Represents consumption for: {winter_days_covered} winter days', fontsize=tamano_small)

ax.xaxis.set_label_text("")

ax.set_ylabel("GWh/d")


ax.grid(which='major', color='#DDDDDD',linestyle='--', linewidth=0.8)

ax.set_axisbelow(True)


plt.savefig(f'figures/EU_LNG_capacities.jpg', dpi=300, bbox_inches='tight') 

