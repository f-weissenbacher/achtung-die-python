import matplotlib.pyplot as plt

def plot_shapely_object(shp, ax=None, show=False):
    import geopandas as gpd
    gs = gpd.GeoSeries(shp)
    p = gs.plot(ax=ax)

    if show and ax is None:
        plt.grid()
        plt.axis('equal')
        plt.show(block=True)
    else:
        return p

