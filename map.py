import folium
import rasterio as rio
from pyproj import Transformer
import numpy as np
import os
import json
import shapefile
from skimage.color import rgb2gray

# Create map object
m = folium.Map(location=[22.269, 79.717], zoom_start=5)



# Overlay geotiff file on map

## RGB Image
in_path = '.\\assets\\tif_files\multi_band_new.tif'

with rio.open(in_path) as src:
    
    img = src.read()
        
    src_crs = src.crs['init'].upper()
    min_lon, min_lat, max_lon, max_lat = src.bounds
    
## Conversion from UTM to WGS84 CRS
bounds_orig = [[min_lat, min_lon], [max_lat, max_lon]]

bounds_fin = []
 
for item in bounds_orig:   
    #converting to lat/lon
    lat = item[0]
    lon = item[1]

    bounds_fin.append([lat, lon])

# Finding the centre latitude & longitude    
centre_lon = bounds_fin[0][1] + (bounds_fin[1][1] - bounds_fin[0][1])/2
centre_lat = bounds_fin[0][0] + (bounds_fin[1][0] - bounds_fin[0][0])/2

img1 = img.transpose(1, 2, 0)



overlay_image = folium.raster_layers.ImageOverlay(img1, opacity=1, 
                                 bounds = bounds_fin)
overlay_image.add_to(m)



# Display India state boundaries as geojson file
style_function = lambda x: {
    "fillColor": "#cacade",
    "color": "#050f1f",
    "weight": "1"}

folium.GeoJson('.//assets/india_state_boundary/New_India_State_Boundary.geojson', name='India', zoom_on_click=True, style_function=style_function).add_to(m)

# # Circle marker for Bengaluru
# folium.Circle(
#     location=[12.97,77.59],
#     radius=30000,
#     popup='Bengaluru',
#     # color='#428bca',
#     # fill=True,
#     fill_color='#f5f5f5',
#     opacity=0.0
# ).add_to(m)



# Generate map
m.save('map.html')