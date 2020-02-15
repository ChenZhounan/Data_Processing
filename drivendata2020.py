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

# load our training and test catalogs
train1_cat = Catalog.from_file('https://drivendata-competition-building-segmentation.s3-us-west-1.amazonaws.com/train_tier_1/catalog.json')
#train2_cat = Catalog.from_file('https://drivendata-competition-building-segmentation.s3-us-west-1.amazonaws.com/train_tier_2/catalog.json')
#test_cat = Catalog.from_file('https://drivendata-competition-building-segmentation.s3-us-west-1.amazonaws.com/test/catalog.json')

# make a dict of all collections witinin train1 catalog
cols = {cols.id:cols for cols in train1_cat.get_children()}
cols['acc'].to_dict()
# for all items within acc col, either load and display label geojson with geopandas or raster metadata with rasterio

for i in cols['acc'].get_all_items():
    print(i.id, '\n----------------------------')
    pprint(i.properties)
    if 'label' in i.id:

        gdf = gpd.read_file(i.make_asset_hrefs_absolute().assets['labels'].href)
        #gdf.plot()
        #plt.show()
    else:
        print('raster metadata:')
        pprint(rasterio.open(i.make_asset_hrefs_absolute().assets['image'].href).meta)
    print('\n----------------------------')

