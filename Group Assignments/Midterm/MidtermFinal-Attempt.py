#!/usr/bin/env python
# coding: utf-8

# # Mapping Pollution and Disinvested Census Tracts in Los Angeles County
# 
# What areas have a concentration of pollution in Los Angeles? What low-income census tracts are more vulnerable to the effects of climate change according to CalEPA?
# 

# In[10]:


import pandas as pd

# to plotting things with plotlyimport plotly.express as px
import plotly.express as px


#importing my first data set
df= pd.read_csv('CalEnviro_LA_County.csv')


# # Exploring the Data

# In[11]:


df.shape


# In[12]:


df.head(10)


# # Changing the data type
# 

# In[13]:


# Changed Census tract to string values 
df['Census Tract'] = df['Census Tract'].astype(str)


# In[14]:


# Adding a zero to the Census Tract Column
df['Census Tract'] = df['Census Tract'].str.zfill(11)


# In[15]:


df.shape


# In[6]:


df.head(10)


# # Creating a new data frame

# In[16]:


#Cleaned data that was not Los Angeles County

df_LA= df[df['California County']== 'Los Angeles'].copy()


# In[17]:


df_LA.shape


# In[18]:


#Checking the new data frame 
df_LA.head(10)


# In[8]:


# What columns do I have?
df.columns


# In[20]:


# renaming the columns

df_LA=df_LA.rename(columns={"CalEnviroScreen\n3.0 Score": "Vulnerability Score", 
                          "CalEnviroScreen 3.0 \nPercentile Range": "Percentile Range",
                          "Pollution Burden\nPercentile" : "Burden Percentile",
                          "Population Characteristics\nPercentile" : "Characteristcs Percentile",
                          "Total Population" : "Population",
                          "Nearby City \n(to help approximate location only)" : "Nearby City"
                         })

#check out the renamed columns
df_LA.head(10)


# In[13]:


df_LA.head()


# # Charting data

# <div class="alert alert-danger">
# Just to be sure, sort the data first.
# </div>

# In[21]:


#sort it first
df_LA = df_LA.sort_values(by='Vulnerability Score',ascending=False)


# In[22]:


df_LA.head(10)


# In[23]:


# First attempt of a chart
df_LA.head(10).plot.bar(x='Approximate Zip Code',
                            y='Vulnerability Score', 
                            title='Top 10 Zip codes with Highest Vulnerability Score')


# In[17]:


df_LA.info()


# In[24]:


# Second attempt of a prettier bar chart using plotly 
import plotly.express as px


# In[25]:


df_LA.iloc[:10]


# <div class="alert alert-danger">
# Instead of Zipcode (which is only approximate), it is the top census tracts. 
# </div>

# In[28]:


#Creating a Census Tracts Bar Chart with the top 10 Highest Vulnerability Scores

fig = px.bar(df_LA.iloc[:10], 
             x='Census Tract', 
             y='Vulnerability Score', 
             text= 'Vulnerability Score', 
             color='Vulnerability Score', 
             height=600, 
             title='Top 10 Census Tracts with Highest Vulnerability Score')

fig.update_layout(xaxis=dict(type='category'))

fig.show()


# # Let's map it now! - Importing geopandas 

# In[29]:


import geopandas as gpd


# In[30]:


#importing my geographic portion of the data

tracts= gpd.read_file('census-tracts-2012-Copy1.geojson')
tracts.head()


# In[32]:


# Let's only use the columns needed for mapping
tracts = tracts[['name','geometry']]
tracts.head()


# In[33]:


# renaming the columns to be able to merge
tracts.columns = ['Census Tract','geometry']
tracts.head()


# In[34]:


# Getting our base map
tracts.plot(figsize=(12,12))


# # Merging Geopandas and CalEnviroScreen dataframes

# In[35]:


# create a new dataframe based on the joined data

combined_tracts= df_LA.merge(tracts,on='Census Tract', how='left')


# show me the first 5 to make sure it worked
combined_tracts.head()


# In[36]:


# Now let's convert the merged dataframeinto a geodataframe
combined_tracts = gpd.GeoDataFrame(combined_tracts)


# In[39]:


# Getting some basic stats
combined_tracts['Vulnerability Score'].describe()


# Looks like the vulnerability score ranges from about 39.3-80.7, with an average score of about 52

# # First Map!!

# In[37]:


combined_tracts.plot(figsize=(12,12))


# In[42]:


# First data map for the Vulnerability Score
combined_tracts.plot(figsize=(20,20),column='Vulnerability Score',
                 legend=True,
                 cmap='RdBu_r',
                 vmin=0)


# In[44]:


# Importing a new library to add a basemap

import contextily as ctx


# In[45]:


# reproject to web mercator- Still learning why
combined_tracts = combined_tracts.to_crs(epsg=3857)


# In[48]:


#Mapping the pollution variable (won't use for final)
ax = combined_tracts.plot(figsize=(20,20),
                 column='Percentile Range',
                 legend=True,
                 cmap='RdBu_r'
                 )
ax.axis('off')
ctx.add_basemap(ax,source=ctx.providers.CartoDB.Positron)


# #Finally Done!! 

# In[ ]:




