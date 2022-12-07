#Step 1: Import the data and coordinates 
#Step 2: Put coordinates into a dataframe and subsequently a geodataframe
#Step 3: Match the coordinates with the object ID (hives)
#Step 4: Project the shapefile and coordinates
#Step 5: Create a function to perform statistical analsysis on the elements
#Step 6: Put buffer around the beehives
#Step 7: Create a graduated symbols map of the point data

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import fiona
import os

#read shapefile
shapefile = gpd.read_file("./Superfund_Shape/Superfund_Shape.shp")
denver = gpd.read_file("./denver/denver.shp")

#read coordinate and elements data
hmsdf = pd.read_csv('./Heavy Metal Sheet-Final.csv')
elementsdf = hmsdf.iloc[: , 3:12].copy()
coord = hmsdf.iloc[: , [12,13]].copy()
elnames = elementsdf.columns

#convert coordinates dataframe to geodataframe
coords_gdf = gpd.GeoDataFrame(coord, geometry=gpd.points_from_xy(hmsdf.Coordinate2, hmsdf.Coordinate1))
hms_gdf = gpd.GeoDataFrame(hmsdf, geometry=gpd.points_from_xy(hmsdf.Coordinate2, hmsdf.Coordinate1))

def elstats (df, eldf):
  """
  Statistics for mean, median, etc. from a pandas dataframe that contains elemental data
  parameters:
    df: the name of the dataframe with the data
    eldf: list of the element names

  """
  mean = df.mean()
  stddev = df.std()
  max = df.max()
  min = df.min()
  
  for i in range(len(elnames)):
    print(f"{eldf[i]}: mean = {round(mean[i], 2)}, standard deviation = {round(stddev[i], 2)}, max = {round(max[i], 2)}, min = {round(min[i], 2)}")
  


elstats(elementsdf, elnames)

#set the initial geodataframe crs
#WGS 84 / Pseudo-Mercator -- Spherical Mercator
coords_gdf.crs = "EPSG:3857"

#convert coordinates to a Colorado specific projection
shapefile = shapefile.to_crs("EPSG:3857")
denver = denver.to_crs("EPSG:3857")

#buffer for 3 miles in meters
buffer = coords_gdf.buffer(4828.03)
buffer = gpd.GeoDataFrame(gpd.GeoSeries(buffer))
buffer = buffer.rename(columns={0: 'geometry'})
buffer = buffer.set_geometry('geometry')

intersection = gpd.overlay(buffer, shapefile, how='intersection')

intersection.to_file('sf_overlap.shp')


#create a geodataframe of only the superfund sites that intersect
superfund = []
for id1 in range(len(intersection)):
    for id2 in range(len(shapefile)):
        if shapefile['ID'][id2] == intersection['ID'][id1]:
            xy = shapefile['geometry'][id2]
            superfund.append(xy) 

superfunddf = pd.DataFrame(superfund)
superfunddf = superfunddf.rename(columns={0: 'geometry'})
superfundgdf = gpd.GeoDataFrame(superfunddf, geometry='geometry')

#create maps showing the extent of contamination for each element
lred = mpatches.Patch(color='red', label='Superfund Site/Hive Overlap')
lblue = mpatches.Patch(color='blue', label='Superfund Site')
lyellow = mpatches.Patch(color='yellow', label="Range of Hive")
lblack = mpatches.Patch(color='black', alpha=0.5, label="Extent of Contamination")
for el in elnames:
    fig, ax = plt.subplots(figsize=(10,10))
    fig.suptitle(f'Extent of {el} Contamination in Denver Hives', fontsize=25)
    ms = hms_gdf[el]
    superfundgdf.plot(ax=ax, color='blue')
    buffer.plot(ax=ax, color='yellow')
    intersection.plot(ax=ax, color='red')
    hms_gdf.plot(markersize=ms * 20, ax=ax, color='black', alpha=0.5)
    denver.plot(ax=ax, facecolor="none")
    fig.legend(handles=[lblue, lred, lyellow, lblack], fontsize=10, frameon=True, loc='center right', title="LEGEND")
    ax.set_axis_off()

plt.show()