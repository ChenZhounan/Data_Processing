import os
os.environ["CURL_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

from matplotlib import pyplot as plt
import numpy as np
from pprint import pprint

import rasterio
from rasterio.windows import Window
import geopandas as gpd

from pystac import (Catalog, CatalogType, Item, Asset, LabelItem, Collection)

# overwriting STAC_IO read method to handle http/s as per https://pystac.readthedocs.io/en/latest/concepts.html#using-stac-io

from urllib.parse import urlparse
import requests
from pystac import STAC_IO

def my_read_method(uri):
    parsed = urlparse(uri)
    if parsed.scheme.startswith('http'):
        return requests.get(uri).text
    else:
        return STAC_IO.default_read_text_method(uri)
STAC_IO.read_text_method = my_read_method
train1_cat = Catalog.from_file('https://drivendata-competition-building-segmentation.s3-us-west-1.amazonaws.com/train_tier_1/catalog.json')


# make a dict of all collections witinin train1 catalog
cols = {cols.id:cols for cols in train1_cat.get_children()}
cols
cols['acc'].to_dict()
# for all items within acc col, either load and display label geojson with geopandas or raster metadata with rasterio
# iterate through all the items within acc collection and print their ids
for i in cols['acc'].get_all_items():
  print(i.id)

# open one image item
SCENE_ID = 'ca041a'
one_item = cols['acc'].get_item(id=SCENE_ID)
one_item.to_dict()


# load raster for this item
rst = rasterio.open(one_item.assets['image'].href)
rst.meta

# check raster resolution
rst.res

# make a windowed read of this raster and reshape into a displayable 4-d array (RGB+alpha channel)
# more on windowed reads with rasterio: https://rasterio.readthedocs.io/en/stable/topics/windowed-rw.html#windows

win_sz = 1024

window = Window(rst.meta['width']//2,rst.meta['height']//2,win_sz,win_sz) # 1024x1024 window starting at center of raster
win_arr = rst.read(window=window)
win_arr = np.moveaxis(win_arr,0,2)
plt.figure(figsize=(10,10))
plt.imshow(win_arr)

