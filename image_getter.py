import io
import math
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class ImageGetter():
    def __init__(self, ):
        self.username = 
        self.password = 
        self.connectid = 

    def get_image(self, lat, lon):
        xTile, yTile = self.get_tile_indexes(lat, lon)
        self.get_image_from_maxar(xTile, yTile)
        return

    def get_image_from_address(self, address):
        lat, lon = self.get_coordinates(address)
        xTile, yTile = self.get_tile_indexes(lat, lon)
        self.get_image_from_maxar(xTile, yTile)
        return

    def get_coordinates(self, address):
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        return float(response[0]["lat"]), float(response[0]["lon"])

    def get_tile_indexes(self, lat, lon):
        lat_rad = math.radians(lat)
        n = 2.0 ** 18
        xtile = int((lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def get_image_from_maxar(self, col, row):
        url = f"https://securewatch.maxar.com/earthservice/wmtsaccess?SERVICE=WMTS"\
        + f"&VERSION=1.0.0"\
        + f"&STYLE="\
        + f"&REQUEST=GetTile"\
        + f"&CONNECTID={self.connectid}"\
        + f"&LAYER=DigitalGlobe:ImageryTileService"\
        + f"&FORMAT=image/jpeg"\
        + f"&TileRow={row}"\
        + f"&TileCol={col}"\
        + f"&TileMatrixSet=EPSG:3857"\
        + f"&TileMatrix=EPSG:3857:18"\
        + f"&featureProfile=Consumer_Profile"\
    
        response = requests.get(url, auth=(self.username, self.password))
        image = np.array(Image.open(io.BytesIO(response.content)))
        plt.imsave("image.jpg", image)
        plt.imshow(image)
        return

image_getter = ImageGetter()
image_getter.get_image_from_address('')

import urllib.parse

address = '6 scarlet close london'
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

response = requests.get(url).json()
print(response[0]["lat"])
print(response[0]["lon"])

!pip geopandas -v

import geopandas as gpd

gdf = gpd.read_file('/content/beyond.geojson')
gdf.set_crs('EPSG:4326')
gdf.to_crs('EPSG:3857')
gdf.to_file("reprojected.geojson", driver='GeoJSON')
gdf

{
"type": "FeatureCollection",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features": [
{ "type": "Feature", "properties": { }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -100.007063898533843, 34.372562780476954 ], [ -100.008142429773699, 34.369910677253372 ], [ -100.007311061942517, 34.366460962813974 ], [ -100.000660119295333, 34.365626333141861 ], [ -99.999177138839769, 34.36813019721582 ], [ -100.001334201320091, 34.372154770061513 ], [ -100.007063898533843, 34.372562780476954 ] ] ] } },
{ "type": "Feature", "properties": { }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -99.99899738363294, 34.373323158220316 ], [ -99.999626526856289, 34.370188873841116 ], [ -99.99695266815705, 34.368909161888311 ], [ -99.99899738363294, 34.373323158220316 ] ] ] } }
]
}

gdf.bounds.to_numpy()[0]

gdf.to_json()
