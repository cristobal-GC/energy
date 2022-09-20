# -*- coding: utf-8 -*-
"""
This script generates a plot showing LNG send-out capacities in EU countries

@author: cristobal-GC
"""


import pandas as pd
import matplotlib.pyplot as plt





#################### Analysis parameters

### EU, SP and PT gas annual consumption 
# Ref: https://agsi.gie.eu/
EU_year_cons = 4151.8 # TWh
ES_year_cons =  372.7 # TWh
PT_year_cons =   68.9 # TWh


### Export capacity ES-FR
export_capacity_ES_FR = 226 # GWh/d


### Winter consumption (from 1/Nov to 31/March) is assumed to be 55% of year consumption
# Ref: EUROSTAT
# https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gasm/default/table?lang=en
winter_cons_factor = 0.55
winter_days = 151





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
color_bar 		= (0.3,0.5,0.0) # green
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



### Message 1
if token_add_message_1:
	
	# Get total capacity in EU 
	EU_LNG_capacity = dfEU.loc[0,['DTRS (GWh/d)']].item()

	# Add message
	ax.text(2.25, 1550, f'EU total regasification capacity: {round(EU_LNG_capacity/10)/100} TWh/d', 
			fontsize=tamano, color=color_message)



### Message 2
if token_add_message_2:

	# Get total capacity in EU 
	EU_LNG_capacity = dfEU.loc[0,['DTRS (GWh/d)']].item()

	# Get total capacity in EU without ES and PT LNG capacity, but with ES-FR pipeline
	ES_LNG_capacity = df[df.Name=='Spain']['DTRS (GWh/d)'].item()
	PT_LNG_capacity = df[df.Name=='Portugal']['DTRS (GWh/d)'].item()
	EU_LNG_capacity_reduced = EU_LNG_capacity-ES_LNG_capacity-PT_LNG_capacity+export_capacity_ES_FR

	# Get UE gas annual consumption without ES and PT
	EU_year_cons_reduced = EU_year_cons-ES_year_cons-PT_year_cons

	# EU gas consumption in winter period
	EU_winter_cons = EU_year_cons*winter_cons_factor

	# EU gas consumption in winter period without ES and PT
	EU_winter_cons_reduced = EU_year_cons_reduced*winter_cons_factor

	# Winter days covered with NGL capacity
	winter_days_covered = round(winter_days*(EU_LNG_capacity*winter_days/(EU_winter_cons*1000)))

	# Winter days covered with NGL capacity considering limited pipeline capacity between ES-FR
	winter_days_covered_reduced = round(winter_days*(EU_LNG_capacity_reduced*winter_days/(EU_winter_cons_reduced*1000)))

	# Add message
	ax.text(2.5,1350,f'Allows for covering: {winter_days_covered} winter days ({winter_days_covered_reduced} winter days)' u"$^\u2020$",
			fontsize=tamano_small, color=color_message)



### Notes
ax.text(-1.5,-850,f'Winter days: From 1/Nov to 31/March (151 days).',
			fontsize=tamano_notes, color=color_notes)

ax.text(-1.5,-950,u'$^\u2020$' f'If pipeline capacity between Spain-France is considered ({export_capacity_ES_FR} GWh/d).',
			fontsize=tamano_notes, color=color_notes)

ax.text(-1.5,-1050,'Data source, details and code: https://alsi.gie.eu/',
			fontsize=tamano_notes, color=color_notes)



### Customise plot

# Add title
plt.title('LNG regasification capacity in EU countries',fontsize = tamano,fontweight="bold")

# Set axes labels
ax.set_xlabel("")
ax.set_ylabel("GWh/d")

# Set grid
ax.grid(which='major', color=color_grid,linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)





#################### Save plot

plt.savefig(f'figures/EU_LNG_capacities.jpg', dpi=300) 



