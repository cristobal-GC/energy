# -*- coding: utf-8 -*-
"""
This script generates a plot showing the current state of gas storage facilities in EU

https://github.com/cristobal-GC/energy
"""

# Comment: only Spain and Latvia can withdraw during winter days (1/Nov to 31/March) less than their total storage capacity due to limited withdrawal capacity. This fact is negligeable.

# Comment: minimum EU storage level 18% in April 2018



import pandas as pd
import matplotlib.pyplot as plt



#################### Analysis parameters

### Date for file data/AGSI_CountryAggregatedDataset_gasDayStart_{year}-{month}-{day}
day		= '17'
month	= '09'
year	= '2022'



### Winter consumption (from 1/Nov to 31/March) is assumed to be 55% of year consumption
# Ref: EUROSTAT
# https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gasm/default/table?lang=en
winter_cons_factor = 0.55
winter_days = 151



### Minimum storage level in EU wrt total capacity (April/2018): 18%
# Ref: https://agsi.gie.eu/
min_storage_level = 0.18



### EU gas annual consumption 
# Ref: https://agsi.gie.eu/
EU_year_cons = 4151.8 # TWh





#################### Plot parameters

### tokens
token_add_message_1 = True
token_add_message_2 = True



### font sizes
tamano 			= 18
tamano_small 	= 16
tamano_notes	= 13

params = {'axes.labelsize': tamano,
          'xtick.labelsize': tamano,
          'ytick.labelsize': tamano}     

plt.rcParams.update(params)



### Colours
color_bar 		= (0.8,0.4,0.4) # dark red
color_message 	= (0.0,0.3,0.6) # azure 40%
color_grid		= (0.8,0.8,0.8) # light gray
color_notes		= (0.4,0.4,0.4) # gray



### Define figure and axes size
figure_width 	= 30 # cm
figure_height 	= 20 # cm

left_margin 	= 3 # cm
right_margin 	= .5 #cm
top_margin 		= 1 # cm
bottom_margin 	= 7 # cm





#################### Data processing to obtain dataframes 'df' and 'dfEU'

### Read data
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
df = df2.sort_values("Working (gas) volume (TWh)",ascending=False)

# Select EU row
dfEU = df1[data["Name"]=="EU"][labels_selected]





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
df.plot(x='Name', y='Working (gas) volume (TWh)',
        color=color_grid,
        kind='bar',width=.9,
        legend=None,
        ax=ax)
            

df.plot(x='Name', y='Gas in storage (TWh)',
        color=color_bar,
        kind="bar",width=.9,
        ax=ax,legend=None)



### Message 1
if token_add_message_1:
	
	# Get storage perc in EU 
	porc_EU = dfEU.loc[0,['Full (%)']].item()
	# Add message
	ax.text(4.4, 205, f'EU storage level: {porc_EU}%', fontsize=tamano, color=color_message)



### Message 2
if token_add_message_2:

	# Consumption in 1 winter day
	cons_1winter_day = EU_year_cons*winter_cons_factor/winter_days
	# Winter days covered given current storage and considering minimum storage level
	stored_EU = dfEU.loc[0,['Gas in storage (TWh)']].item()
	winter_days_covered = round((stored_EU*(1-min_storage_level))/cons_1winter_day)
	# Add message
	ax.text(5, 180, f'Gas consumption coverage: {winter_days_covered} winter days',
			fontsize=tamano_small, color=color_message)



### Notes
new_line = 15

ax.text(-2.,-125,f'Winter days: From 1/Nov to 31/March (151 days).',
			fontsize=tamano_notes, color=color_notes)

ax.text(-2.,-125-1*new_line,'Data, details and code:',
			fontsize=tamano_notes, color=color_notes)
ax.text(1.7,-125-1*new_line,'https://github.com/cristobal-GC/energy/blob/main/EU_gas_storage.py',
			fontsize=tamano_notes, color=color_message)



### Customise plot

# Add title
plt.title(f'Gas storage capacity in EU countries on {day}/{month}/{year}',fontsize = tamano,fontweight="bold")

# Set axes labels
ax.set_xlabel("")
ax.set_ylabel("TWh")

# Set grid
ax.grid(which='major', color=color_grid,linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)





#################### Save plot

plt.savefig(f'figures/EU_gas_storage_{year}_{month}_{day}.jpg', dpi=300) 

