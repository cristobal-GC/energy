# -*- coding: utf-8 -*-
"""
This script generates a plot showing gas imports in EU by pipelines
Data source: https://transparency.entsog.eu/#/map

https://github.com/cristobal-GC/energy
"""



import pandas as pd
import matplotlib.pyplot as plt
import textwrap




#################### Analysis parameters

### Winter consumption (from 1/Nov to 31/March) is assumed to be 55% of year consumption
# Ref: EUROSTAT
# https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gasm/default/table?lang=en
winter_cons_factor = 0.55
winter_days = 151

### EU, SP and PT gas annual consumption 
# Ref: https://agsi.gie.eu/
EU_year_cons = 4151.8 # TWh



#################### Plot parameters

### tokens
token_add_message = True



### font sizes
tamano 			= 18
tamano_small 	= 16
tamano_notes	= 13

params = {'axes.labelsize': tamano,
          'xtick.labelsize': tamano,
          'ytick.labelsize': tamano,
		  'legend.fontsize': tamano_notes}     

plt.rcParams.update(params)



### Colours
color_bar 		= (0.5,0.0,1.0) # purple
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



### Max. width of xlabels
max_width = 12





#################### Data processing to obtain dataframes 'df' and 'dfEU'

### Read data
data = pd.read_csv('data/pipelines_EU.csv',delimiter=';',skiprows=1)

# Columns description:
#	'Capacity (GWh/d)'				: Firm capacity
#	'Mean flow last winter (GWh/d)'	: During period 01/11/2021-31/03/2022


# Sort by pipeline capacity
df = data.sort_values("Capacity (GWh/d)",ascending=False)





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
df.plot(x='Name', y="Capacity (GWh/d)",
        color=color_grid,
        kind='bar',width=.9,
        label='Capacity',
        ax=ax)


df.plot(x='Name', y="Mean flow last winter (GWh/d)",
        color=color_bar,
        kind='bar',width=.9,
        label='Mean flow winter 2021',
        ax=ax)



### Message
if token_add_message:
	
	# Get total capacity in EU 
	EU_pipeline_capacity = df['Capacity (GWh/d)'].sum()

	# EU gas consumption in winter period
	EU_winter_cons = EU_year_cons*winter_cons_factor

	# Winter days covered with pipelines capacity
	winter_days_covered = round(winter_days*(EU_pipeline_capacity*winter_days/(EU_winter_cons*1000)))

	# Add message
	ax.text(1.75, 2600, f'Gas consumption coverage: {winter_days_covered} winter days', 
			fontsize=tamano_small, color=color_notes)

	# Get mean imports last winter
	EU_import_last_winter = df['Mean flow last winter (GWh/d)'].sum()

	# Winter days covered assuming winter 2021 imports
	winter_days_covered_2021 = round(winter_days*(EU_import_last_winter*winter_days/(EU_winter_cons*1000)))

	# Add message
	ax.text(1.75, 2200, f'Gas consumption coverage: {winter_days_covered_2021} winter days',
			fontsize=tamano_small, color=color_bar)



### Notes
new_line = 225

ax.text(-1.1,-1550,f'Winter days: From 1/Nov to 31/March (151 days).',
			fontsize=tamano_notes, color=color_notes)

ax.text(-1.1,-1550-new_line,f'Norway pipelines capacity is not included.',
			fontsize=tamano_notes, color=color_notes)

ax.text(-1.1,-1550-2*new_line,'Data, details and code:',
			fontsize=tamano_notes, color=color_notes)

ax.text(0.05,-1550-2*new_line,'https://github.com/cristobal-GC/energy/blob/main/EU_pipelines.py',
			fontsize=tamano_notes, color=color_message)


### Customise plot

# Add title
plt.title('Gas import pipelines in EU',fontsize = tamano,fontweight="bold")

# Set axes labels
ax.set_xlabel("")
ax.set_ylabel("GWh/d")

# Set grid
ax.grid(which='major', color=color_grid,linestyle='--', linewidth=0.8)
ax.set_axisbelow(True)

ax.set_xticklabels(textwrap.fill(x.get_text(), max_width) for x in ax.get_xticklabels())



#################### Save plot

plt.savefig(f'figures/EU_pipelines.jpg', dpi=300) 



