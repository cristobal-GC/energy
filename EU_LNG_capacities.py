# -*- coding: utf-8 -*-
"""
This script generates a plot showing LNG regasification capacity in EU countries

Data source:
[1] https://alsi.gie.eu/#/
[2] https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gas/default/table?lang=en
[3] https://ec.europa.eu/eurostat/databrowser/view/nrg_cb_gasm/default/table?lang=en


https://github.com/cristobal-GC/energy
"""



import pandas as pd
import matplotlib.pyplot as plt





#################### Analysis parameters

### Winter days from 1st/Nov to 31/Mar
winter_days = 151


### EU27, SP and PT gas annual consumption (average between 2017 and 2021)
# Ref: EUROSTAT [2]
EU_year_cons = 4287.4 # TWh
ES_year_cons =  638.6 # TWh
PT_year_cons =   66.8 # TWh


### Export capacity ES-FR (pipeline)
export_capacity_ES_FR = 226 # GWh/d


### Winter consumption (from 1/Nov to 31/March) is assumed to be 55% of year consumption
# Ref: EUROSTAT [3]
winter_cons_factor = 0.55





#################### Plot parameters

### tokens
token_add_message = True


### font sizes
tamano 		= 18
tamano_small 	= 16
tamano_notes	= 13

params = {'axes.labelsize': tamano,
          'xtick.labelsize': tamano,
          'ytick.labelsize': tamano}     

plt.rcParams.update(params)


### Colours
color_bar 		= (0.25,0.45,0.0) # green
color_message 		= (0.0,0.3,0.6) # azure 40%
color_grid		= (0.8,0.8,0.8) # light gray
color_notes		= (0.4,0.4,0.4) # gray


### Define figure and axes size
figure_width 	= 30 # cm
figure_height 	= 20 # cm

left_margin 	= 3 # cm
right_margin 	= .5 #cm
top_margin 	= 1 # cm
bottom_margin 	= 7 # cm





#################### Data processing to obtain dataframes 'df' and 'dfEU'

### Read data 
# Source: [1]
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
if token_add_message:
	
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

	# Winter days covered with LNG capacity
	winter_days_covered = round(winter_days*(EU_LNG_capacity*winter_days/(EU_winter_cons*1000)))


	# Winter days covered with LNG capacity considering limited pipeline capacity between ES-FR
	winter_days_covered_reduced = round(winter_days*(EU_LNG_capacity_reduced*winter_days/(EU_winter_cons_reduced*1000)))

	# Add message
	ax.text(2.1, 1550, f'Gas consumption coverage (unconstrained)$^\u2020$: {winter_days_covered} winter days', 
			fontsize=tamano_small, color=color_notes)

	# Add message
	ax.text(2.1,1350,f'Gas consumption coverage (constrained)$^\u2020$    : {winter_days_covered_reduced} winter days',
			fontsize=tamano_small, color=color_bar)



### Notes
new_line = 120

ax.text(-1.5,-850,f'Winter days: From 1/Nov to 31/March (151 days).',
			fontsize=tamano_notes, color=color_notes)

ax.text(-1.5,-850-new_line,u'$^\u2020$' f' Constrained: Exports from Spain to France are limited by pipeline capacity  ({export_capacity_ES_FR} GWh/d).',
			fontsize=tamano_notes, color=color_notes)

ax.text(-1.5,-850-2*new_line,'Data, details and code:',
			fontsize=tamano_notes, color=color_notes)
ax.text(0.7,-850-2*new_line,'https://github.com/cristobal-GC/energy/blob/main/EU_LNG_capacities.py',
			fontsize=tamano_notes, color=color_message)


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



