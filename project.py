import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
#import geopandas as gpd

#Getting the data. The data has millions of rows so choose what can be computed on the machine
response = requests.get('https://data.buffalony.gov/resource/n4ni-uuec.json?$limit=99999')

if response.status_code == 200:
    json_data = response.json()
  
    data = pd.DataFrame(json_data)
    print("Shape before NA removal: ",data.shape)


    data['latitude'] = pd.to_numeric(data['latitude'])
    data['longitude'] = pd.to_numeric(data['longitude'])

    df = data

    numeric_columns = ['dbh', 'total_yearly_eco_benefits', 'stormwater_benefits',
                       'stormwater_gallons_saved', 'greenhouse_co2_benefits',
                       'co2_avoided_in_lbs', 'co2_sequestered_in_lbs', 'energy_benefits',
                       'kwh_saved', 'therms_saved', 'air_quality_benefits',
                       'pollutants_saved_in_lbs', 'property_benefits', 'leaf_surface_area_in_sq_ft']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')


    df.drop(columns=[':@computed_region_fk4y_hpmh',':@computed_region_eziv_p4ck', ':@computed_region_tmcg_v66k',
        ':@computed_region_kwzn_pe6v', ':@computed_region_xbxg_7ifr',
        ':@computed_region_nmyf_6jtp', ':@computed_region_jdfw_hhbp',
        ':@computed_region_h7a8_iwt4', ':@computed_region_ff6v_jbaa',
        ':@computed_region_vsen_jbmg'],inplace=True)
    

    for col in df.columns:
        df = df[df[col] != "VACANT"]

    print("Shape after NA removal:",df.shape)
else:
    print('Request failed with status code:', response.status_code)


# Plot a correlation heatmap of numeric columns
plt.figure(figsize=(12, 10))
sns.heatmap(data[numeric_columns].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Numeric Columns')
plt.show()

# Create a scatter plot of tree locations
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x=df['longitude'], y=df['latitude'], color="green")
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Tree Locations')
plt.show()

# Calculate and plot the number of trees by species
species_counts = df['common_name'].value_counts().reset_index()
species_counts.columns = ['Species', 'Count']
plt.figure(figsize=(12, 8))
sns.barplot(data=species_counts, x=species_counts['Species'][:10], y=species_counts['Count'][:10])
plt.xlabel('Species')
plt.ylabel('Count')
plt.title('Number of Trees by Species')
plt.xticks(rotation=90)
plt.show()

# Calculate and plot the top 10 common tree species
top_species = df['common_name'].value_counts().head(10)
plt.figure(figsize=(10, 8))
sns.barplot(x=top_species.values, y=top_species.index)
plt.xlabel('Count')
plt.ylabel('Species')
plt.title('Top 10 Common Tree Species')
plt.show()


# Filter the DataFrame for the top 10 tree species based on CO2 avoided
top_10_species = df.groupby('common_name')['co2_avoided_in_lbs'].sum().nlargest(10).index
filtered_df = df[df['common_name'].isin(top_10_species)]

# Create a bar plot to compare CO2 avoided for the top 10 species
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_df, x='common_name', y='co2_avoided_in_lbs')
plt.xticks(rotation=45)
plt.xlabel('Tree Species')
plt.ylabel('CO2 Avoided (lbs)')
plt.title('Top 10 Tree Species by CO2 Avoided')
plt.show()

# Filter the DataFrame for the top 10 tree species based on CO2 avoided
top_10_species = df.groupby('common_name')['pollutants_saved_in_lbs'].sum().nlargest(10).index
filtered_df = df[df['common_name'].isin(top_10_species)]

# Create a bar plot to compare CO2 avoided for the top 10 species
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_df, x='common_name', y='pollutants_saved_in_lbs')
plt.xticks(rotation=45)
plt.xlabel('Tree Species')
plt.ylabel('Pollutants (lbs)')
plt.title('Polluitants Saved (lbs)')
plt.show()
