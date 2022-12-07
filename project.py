#Step 1: Import the data and coordinates 
#Step 2: Put coordinates into a dataframe and subsequently a geodataframe
#Step 3: Match the coordinates with the object ID (hives)
#Step 4: Project the shapefile and coordinates
#Step 5: Create a function to perform statistical analsysis on the elements
#Step 6: Put buffer around the beehives
#Step 7: Create a graduated symbols map of the point data

import geopandas as gpd
import pandas as pd
import fiona
import matplotlib.pyplot as plt
import os

#read shapefile
shapefile = gpd.read_file("./Superfund_Shape/Superfund_Shape.shp")

#read coordinate and elements data
hmsdata = pd.read_csv('./Heavy Metal Sheet-Final.csv')
hmsdf = pd.DataFrame(hmsdata)
elementsdf = hmsdf.iloc[: , 3:12].copy()
coord = hmsdf.iloc[: , [12,13]].copy()

#convert coordinates dataframe to geodataframe
coords_gdf = gpd.GeoDataFrame(coord, geometry=gpd.points_from_xy(hmsdf.Coordinate2, hmsdf.Coordinate1))


def elstats (df):
  """
  Statistics for mean, median, etc. from a pandas dataframe that contains elemental data
  parameters:
    df: the name of the dataframe with the data

  """
  mean = df.mean()
  stddev = df.std()
  max = df.max()
  min = df.min()
  elnames = df.columns
  for i in range(len(elnames)):
    print(f"{elnames[i]}: mean = {round(mean[i], 2)}, standard deviation = {round(stddev[i], 2)}, max = {round(max[i], 2)}, min = {round(min[i], 2)}")
  


elstats(elementsdf)

#set the initial geodataframe crs
#WGS 84 / Pseudo-Mercator -- Spherical Mercator
coords_gdf.crs = "EPSG:3857"

#convert coordinates to a Colorado specific projection
shapefile = shapefile.to_crs("EPSG:3857")

#buffer for 3 miles in meters
buffer = coords_gdf.buffer(4828.03)
buffer = gpd.GeoDataFrame(gpd.GeoSeries(buffer))
buffer = buffer.rename(columns={0: 'geometry'})
buffer = buffer.set_geometry('geometry')

intersection = gpd.overlay(buffer, shapefile, how='intersection')

intersection.to_file('sf_overlap.shp')