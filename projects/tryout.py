import geopandas as gpd

# read the shapefile
file = gpd.read_file("/home/marcel/Downloads/test/test.shp")
file = file.to_crs({'init': 'epsg:4326'})
print("test")
