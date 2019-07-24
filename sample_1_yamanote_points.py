from io import StringIO
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

text = """\
name,lat,lng
東京,35.681382,139.766084
有楽町,35.675069,139.763328
新橋,35.665498,139.75964
浜松町,35.655646,139.756749
田町,35.645736,139.747575
品川,35.630152,139.74044
大崎,35.6197,139.728553
五反田,35.626446,139.723444
目黒,35.633998,139.715828
恵比寿,35.64669,139.710106
渋谷,35.658517,139.701334
原宿,35.670168,139.702687
代々木,35.683061,139.702042
新宿,35.690921,139.700258
新大久保,35.701306,139.700044
高田馬場,35.712285,139.703782
目白,35.721204,139.706587
池袋,35.728926,139.71038
大塚,35.731401,139.728662
巣鴨,35.733492,139.739345
駒込,35.736489,139.746875
田端,35.738062,139.76086
西日暮里,35.732135,139.766787
日暮里,35.727772,139.770987
鶯谷,35.720495,139.778837
上野,35.713768,139.777254
御徒町,35.707438,139.774632
秋葉原,35.698683,139.774219
神田,35.69169,139.770883
"""
stream = StringIO(text)
df = pd.read_csv(stream)
# Point(経度, 緯度) あるいは Point(longitude, latitude) として生成する
geometry = [Point(lng, lat) for lng, lat in zip(df['lng'], df['lat'])]
crs = {'init': 'epsg:4326'}  # GPSで得られる緯度・経度（地理座標系）
geo_df = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)

geo_df2 = geo_df.to_crs({'init': 'epsg:3857'}) # 球面(半径6378137m)メルカトル図法

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot()
geo_df2.plot(ax=ax)

# add_basemap(ax, 15)

plt.show()
plt.close()

