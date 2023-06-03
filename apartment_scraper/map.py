import plotly.express as px
import geopandas as gpd
import pandas as pd
from apartment_scraper.models import Model
from apartment_scraper import pkg_path
from shapely.geometry import Point


def create_geo_df() -> gpd.GeoDataFrame:
    d = {
            'name': ['name1', 'name2'],
            'geometry': [
                Point(48.28739771, 16.31984984),
                Point(48.49086202, 15.69899314)
            ]
    }
    return gpd.GeoDataFrame(d)


def setup_figure(geo_df: gpd.GeoDataFrame):
    px.set_mapbox_access_token(open(".mapbox_token").read())
    fig = px.scatter_mapbox(
        geo_df,
        lat=geo_df.geometry.x,
        lon=geo_df.geometry.y,
        hover_name="apartment_id",
        zoom=1
    )
    fig.show()


def plot_map(model: Model):
    engine = model.get_engine()

    with engine.connect() as conn, conn.begin():
        data = pd.read_sql_table(
            "apartments", conn, columns=[
                "id", "apartment_id", "coordinates", "price", "price_per_area"
            ]
        )
    data[['lat', "lon"]] = data['coordinates'].str.split(',', expand=True)
    data['lat'] = pd.to_numeric(data['lat'])
    data['lon'] = pd.to_numeric(data['lon'])
    print(data.head())
    print(data.info())

    gdf = gpd.GeoDataFrame(
        data, geometry=gpd.points_from_xy(data.lat, data.lon)
    )

    # geo_df = create_geo_df()
    setup_figure(gdf)


if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))
    plot_map(model)
