#Step 1: import the data and coordinates 
#Step 2:

import geopandas as gpd
import pandas as pd
import os

# path = 'C:/Users/larsenh/Downloads/'

# coord_list = []
# with open(path + 'Coordinates.txt') as file:
#     for coordinates in file:
#         temp_list = tuple(coordinates.strip().split('\t'))

# elements_list = []
# with open(path + 'Elements.txt') as file:
#     for ele in file:
#         temp_list = tuple(ele.strip().split('\t'))


# coords_df = pd.DataFrame(new_coords, columns=['Longitude', 'Latitude'])
# coords_gdf = gpd.GeoDataFrame(coords_df, geometry = gpd.points_from_xy(coords_df.Longitude, 
#             coords_df.Latitude))

# elements_df = pd.DataFrame(new_elements, columns=['Longitude', 'Latitude'])
# elements_gdf = gpd.GeoDataFrame(elements_df, geometry = gpd.points_from_xy(elements_df.Longitude, 
#             elements_df.Latitude))


# crs = {'init': 'epsg:4326'}
# coords_gdf = gpd.GeoDataFrame(coords_gdf, crs = crs)
# elements_gdf = gpd.GeoDataFrame(elements_gdf, crs = crs)

hmsdata = pd.read_csv('./Heavy Metal Sheet-Final.csv')
hmsdf = pd.DataFrame(hmsdata)
elements = hmsdf.iloc[: , 3:12].copy()
coord = hmsdf.iloc[: , [12,13]].copy()

#read shapefile
shapefile = gpd.read_file("shapefile.shp")

#convert coordinates to Colorado specific projection
beehives_gdf = coords_gdf.to_crs({'init': 'epsg:26954'})
shapefile = shapefile.to_crs({'init': 'epsg:26954'})

#buffer for 3 miles in meters (I think the buffer uses the CRS measurement for calculation, the CRS for EPSG:26954 is in meters so
  #it wants meters for the buffer function
beehives_buffer = beehives_gdf.buffer(4828.03)

#Superfund sites that fall within one of the beehive buffers?
for hive in beehives_buffer:
  hive.intersection(shapefile, align=True)
