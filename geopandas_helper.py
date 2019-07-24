import contextily as ctx
import pyproj

# https://geopandas.readthedocs.io/en/latest/gallery/plotting_basemap_background.html
def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    # EPSG:3857 球面メルカトル図法でのみ利用可能
    # 国土地理院タイルサーバ
    # url='https://cyberjapandata.gsi.go.jp/xyz/pale/tileZ/tileX/tileY.png'
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax

# アスペクト比がどのようになっているか表示する
# GPS 緯度・経度 (EPSG:4326) で描画された figure, axis を引数に指定してください。
def diag_distortion(fig, ax):

    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    axsize_x, axsize_y = bbox.width, bbox.height
    ### print("figsize", figsize_x, figsize_y)
    xlim_0, xlim_1 = ax.get_xlim()
    ylim_0, ylim_1 = ax.get_ylim()

    geod = pyproj.Geod(ellps='WGS84')
    _, _, dist_x = geod.inv(xlim_0, ylim_0, xlim_1, ylim_0)  # x軸方向の距離を取得
    _, _, dist_y = geod.inv(xlim_0, ylim_0, xlim_0, ylim_1)  # y軸方向の距離を取得
    print("inv", dist_x, dist_y)  # x軸方向、y軸方向の距離を表示
    print("diag", dist_x / axsize_x , dist_y / axsize_y, dist_x / axsize_x - dist_y / axsize_y)
                                  # x軸方向、y軸方向の1inchあたりの距離とその差を表示

# アスペクト比が 1:1 に近づくように描画領域を広げます
# GPS 緯度・経度 (EPSG:4326) で描画された figure, axis を引数に指定してください。
def adjust_lim(fig, ax, count=2):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    axsize_x, axsize_y = bbox.width, bbox.height

    for _ in range(count):
        xlim_0, xlim_1 = ax.get_xlim()  # 経度の左端・右端
        ylim_0, ylim_1 = ax.get_ylim()  # 緯度の下端・上端

        geod = pyproj.Geod(ellps='WGS84')
        _, _, dist_x = geod.inv(xlim_0, ylim_0, xlim_1, ylim_0)  # x軸方向の距離を取得
        _, _, dist_y = geod.inv(xlim_0, ylim_0, xlim_0, ylim_1)  # y軸方向の距離を取得

        ideal_dist_y = axsize_y * dist_x / axsize_x  # 理想的なy軸方向の距離を算出
        if dist_y < ideal_dist_y:
            # expand y # y軸方向を大きくする
            ideal_ylim_1 = ylim_0 + (ylim_1 - ylim_0) * ideal_dist_y / dist_y
            delta = ideal_ylim_1 - ylim_1
            ax.set_ylim(ylim_0 - delta / 2, ideal_ylim_1 - delta / 2)  # y軸方向を左右に大きくする
        elif dist_y > ideal_dist_y:
            # expand x # x軸方向を大きくする
            ideal_dist_x = dist_y * axsize_x / axsize_y
            ideal_xlim_1 = xlim_0 + (xlim_1 - xlim_0) * ideal_dist_x / dist_x
            delta = ideal_xlim_1 - xlim_1
            ax.set_xlim(xlim_0 - delta / 2, ideal_xlim_1 - delta / 2)  # x軸方向を左右に大きくする

# plot a scale bar with 4 subdivisions on the left side of the map
# from https://github.com/SciTools/cartopy/issues/490
# 上記URLに投稿されているコードを改変
# EPSG:4326 GPS 緯度・経度なら mercator=False に
# EPSG:3857 球面メルカトル図法なら mercator=True に
def scale_bar_left(ax, mercator=False, horizontal=True, virtical=True,
                   bars=4, length=None, location=(0.1, 0.05), linewidth=3,
                   col='black', barcol='silver', barcol2='dimgrey'):
    """
    ax is the axes to draw the scalebar on.
    mercator is True for mercator coordinates, False for GPS long/lat coordinates.
    horizontal is True to draw the horizontal scale bar.
    virtical is True to draw the virtical scale bar.
    bars is the number of subdivisions of the bar (black and white chunks)
    length is the length of the scalebar in km.
    location is left side of the scalebar in axis coordinates.
    (ie. 0 is the left side of the plot, 1 is the right side of the plot)
    linewidth is the thickness of the scalebar.
    col is the color of the scale bar text
    barcol is the color of the scale bar (first)
    barcol2 is the color of the scale bar (second)
    """
    # Get the limits of the axis in lat long
    llx0, llx1 = ax.get_xlim()  # llx -> limit_long_x  # 経度の左端・右端
    lly0, lly1 = ax.get_ylim()  # lly -> limit_lat_y   # 緯度の下端・上端
    # Get the extent of the plotted area in coordinates in metres
    geod = pyproj.Geod(ellps='WGS84')
    if mercator:  # axは球面メルカトルなので、緯度・経度に直して距離算出
        EPSG3857 = pyproj.Proj(init='EPSG:3857') # 球面メルカトル
        EPSG4326 = pyproj.Proj(init='EPSG:4326') # WGS84 緯度経度
        _t_llx0, _t_lly0 = pyproj.transform(EPSG3857, EPSG4326, llx0, lly0)
        _t_llx1, _t_lly1 = pyproj.transform(EPSG3857, EPSG4326, llx1, lly1)
        _, _, x1 = geod.inv(_t_llx0, _t_lly0, _t_llx1, _t_lly0)  # 経度の左端・右端から距離を算出
        _, _, y1 = geod.inv(_t_llx0, _t_lly0, _t_llx0, _t_lly1)  # 緯度の左端・右端から距離を算出
    else:  # axはGPS 緯度・経度なので、そのまま距離算出
        _, _, x1 = geod.inv(llx0, lly0, llx1, lly0)  # 経度の左端・右端から距離を算出
        _, _, y1 = geod.inv(llx0, lly0, llx0, lly1)  # 緯度の左端・右端から距離を算出

    # Calculate a scale bar length if none has been given
    if not length:
        length = x1 / 5000  # in km
        ndim = int(np.floor(np.log10(length)))  # number of digits in number
        length = round(length, -ndim)  # round to 1sf

        # Returns numbers starting with the list
        def scale_number(x):
            if str(x)[0] in ['1', '2', '5']:
                return int(x)
            else:
                return scale_number(x - 10 ** ndim)

        length = scale_number(length)

    if horizontal:
        # Make tmc aligned to the left of the map,
        # virtically at scale bar location
        sbllx = llx0 + (llx1 - llx0) * location[0]  # sbllx -> scroll_bar_limit_long_x
        sblly = lly0 + (lly1 - lly0) * location[1]  # sblly -> scroll_bar_limit_long_y
        # Generate the x coordinate for the ends of the scalebar
        sbwidth = (llx1 - llx0) * length * 1000 / x1
        bar_xs = [sbllx, sbllx + sbwidth / bars]
        # Plot the scalebar chunks
        _barcol = barcol
        for i in range(0, bars):
            # plot the chunk
            ax.plot(bar_xs, [sblly, sblly], color=_barcol, linewidth=linewidth)
            # alternate the colour
            _barcol = barcol2 if _barcol == barcol else barcol
            # Generate the x coordinate for the number
            bar_xt = sbllx + i * sbwidth / bars
            # Plot the scalebar label for that chunk
            ax.text(bar_xt, sblly + (lly1 - lly0) * (location[1] / 12), str(round(i * length / bars)),
                    horizontalalignment='left', verticalalignment='bottom',
                    color=col)
            # work out the position of the next chunk of the bar
            bar_xs[0] = bar_xs[1]
            bar_xs[1] = bar_xs[1] + sbwidth / bars
        # Generate the x coordinate for the last number
        bar_xt = sbllx + sbwidth
        # Plot the last scalebar label
        ax.text(bar_xt, sblly + (lly1 - lly0) * (location[1] / 12), str(round(length)) + " km",
                horizontalalignment='left', verticalalignment='bottom',
                color=col)

    if virtical:
        # horizontally at scale bar location
        sbllx = llx0 + (llx1 - llx0) * location[1]
        sblly = lly0 + (lly1 - lly0) * location[0]
        # Generate the y coordinate for the ends of the scalebar
        sbwidth = (lly1 - lly0) * length * 1000 / y1
        bar_ys = [sblly, sblly + sbwidth / bars]
        # Plot the scalebar chunks
        _barcol = barcol
        for i in range(0, bars):
            # plot the chunk
            ax.plot([sbllx, sbllx], bar_ys, color=_barcol, linewidth=linewidth)
            # alternate the colour
            _barcol = barcol2 if _barcol == barcol else barcol
            # Generate the y coordinate for the number
            bar_yt = sblly + i * sbwidth / bars
            # Plot the scalebar label for that chunk
            ax.text(sbllx + (llx1 - llx0) * (location[0] / 12), bar_yt, str(round(i * length / bars)),
                    horizontalalignment='left', verticalalignment='bottom',
                    color=col)
            # work out the position of the next chunk of the bar
            bar_ys[0] = bar_ys[1]
            bar_ys[1] = bar_ys[1] + sbwidth / bars
        # Generate the x coordinate for the last number
        bar_yt = sblly + sbwidth
        # Plot the last scalebar label
        ax.text(sbllx + (llx1 - llx0) * (location[0] / 12), bar_yt, str(round(length)) + " km",
                horizontalalignment='left', verticalalignment='bottom',
                color=col)
