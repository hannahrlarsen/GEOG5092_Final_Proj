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
