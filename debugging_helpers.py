import matplotlib.pyplot as plt

def plot_shapely_object(shp, color=None, ax=None, show=False, invert_y=False):
    import geopandas as gpd

    if ax is None:
        ax = plt.gca()

    if isinstance(shp, list):
        n_shapes = len(shp)
        if color is None or len(color) != n_shapes:
            color = [f"C{k}" for k in range(n_shapes)]
        for k,s in enumerate(shp):
            gs = gpd.GeoSeries(s)
            gs.plot(ax=ax, color=color[k])
    else:
        gs = gpd.GeoSeries(shp, color=color)
        gs.plot(ax=ax)

    if invert_y:
        ax.invert_yaxis()

    if show:
        plt.grid()
        plt.axis('equal')
        plt.show(block=True)


