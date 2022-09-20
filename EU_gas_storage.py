# -*- coding: utf-8 -*-
"""
This script generates a plot showing the current state of gas storage facilities in EU
@author: cristobal-GC
"""

# Comment: only Spain and Latvia can withdraw during winter days (1/Nov to 31/March) less than their total storage capacity due to limiting withdrawal capacity

# Comment: minimum EU storage level 18% in April 2018


import pandas as pd
import matplotlib.pyplot as plt


day		= '17'
month	= '09'
year	= '2022'


tamano = 18
tamano_small = 16



# update font size 
params = {'axes.labelsize': tamano,
          'xtick.labelsize': tamano,
          'ytick.labelsize': tamano}     

plt.rcParams.update(params)



my_red = (.8,0.4,0.4)
my_gray = (.77,.77,.77)

##### Winter consumption (from 1/Nov to 31/March) is assumed to be 55% of year consumption
# Ref: EUROSTAT
# https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gasm/default/table?lang=en
winter_cons_factor = 0.55
winter_days = 151

# Minimum storage level in EU wrt total capacity (April/2018): 18%
min_storage_level = 0.18


##### Data processing

# Read data
data = pd.read_csv(f'data/AGSI_CountryAggregatedDataset_gasDayStart_{year}-{month}-{day}.csv',delimiter=';')

# Remove countries with No Data
df0 = data.loc[data["Status"]!="N"]

# Remove countries with very small storage capacity
df1 = df0.loc[df0["Working (gas) volume (TWh)"]>1]


# Select relevant fields
countries_selected=["Austria",
                    "Belgium",
                    "Bulgaria",
                    "Croatia",
                    "Czech Republic",
                    "Denmark",
                    "France",
                    "Germany",
                    "Hungary",
                    "Ireland",
                    "Italy",
                    "Latvia",
                    "Netherlands",
                    "Poland",
                    "Portugal",
                    "Romania",
                    "Slovakia",
                    "Spain",
                    "Sweden"]

labels_selected=["Name",
                 "Gas in storage (TWh)",
                 "Working (gas) volume (TWh)",
                 "Full (%)",
                 "Consumption (TWh)"]

df2 = df1[data["Name"].isin(countries_selected)][labels_selected]


# Sort by storage capacity
df3 = df2.sort_values("Working (gas) volume (TWh)",ascending=False)


# Select EU row
dfEU = df1[data["Name"]=="EU"][labels_selected]



##### Make plot

### Define figure and axes size

figure_width = 30 # cm
figure_height = 20 # cm

left_margin = 3 # cm
right_margin = .5 #cm
top_margin = .2 # cm
bottom_margin = 5.6 # cm

left    = left_margin / figure_width # Percentage from width
right   = right_margin / figure_width # Percentage from width
top     = top_margin / figure_height # Percentage from height
bottom  = bottom_margin / figure_height # Percentage from height

width  = 1 - left - right
height = 1 - top - bottom

cm2inch = 1/2.54 # inch per cm

fig = plt.figure(figsize=(figure_width*cm2inch,figure_height*cm2inch))
ax = fig.add_axes((left, bottom, width, height))




df3.plot(x='Name', y='Working (gas) volume (TWh)',
              color=my_gray,
              kind='bar',width=.9,
              legend=None,
              ax=ax)
            

df3.plot(x='Name', y='Gas in storage (TWh)',
         color=my_red,
         kind="bar",width=.9,
         ax=ax,legend=None)



porc_EU = dfEU.loc[0,['Full (%)']].item()
ax.text(5, 240, f'EU storage level: {porc_EU}%', fontsize=tamano)

# Consumption in 1 winter day
EU_year_cons = max(dfEU.loc[0,['Consumption (TWh)']].item(),4151.8)
cons_1winter_day = EU_year_cons*winter_cons_factor/winter_days
# Winter days covered given current storage and considering minimum storage level
stored_EU = dfEU.loc[0,['Gas in storage (TWh)']].item()
winter_days_covered = round((stored_EU*(1-min_storage_level))/cons_1winter_day)
ax.text(5, 220, f'Represents consumption for: {winter_days_covered} winter days', fontsize=tamano_small)

ax.xaxis.set_label_text("")

ax.set_ylabel("TWh")


ax.grid(which='major', color='#DDDDDD',linestyle='--', linewidth=0.8)

ax.set_axisbelow(True)


plt.savefig(f'figures/EU_storage_{year}_{month}_{day}.jpg', dpi=300, bbox_inches='tight') 

