import plotly.express as px
from utils.names import MapValues


class MapCreator:
    def __init__(self,geo_data):
        self.geojson_data = geo_data
        self.indexes = [feature["properties"]["NAME"] for feature in self.geojson_data["features"]]
        self.values = [0] * len(self.indexes)
        
        self.__draw_map()

    def set_geo_data(self,geo_data):
        self.geojson_data = geo_data
        self.indexes = [feature["properties"]["NAME"] for feature in self.geojson_data["features"]]
        self.values = [0] * len(self.indexes)
        self.__draw_map()

    def set_values(self,values):
        self.values = values
        self.__draw_map()
    def set_indexes(self, indexes):
        self.indexes = indexes
        self.__draw_map()
    def get_map(self):
        return self.map
    def draw_map(self):
        self.__draw_map()
    def __draw_map(self):
        
        fig = px.choropleth(
        #locations = self.countries
        locations = self.indexes,
        geojson=self.geojson_data,
        
        color=self.values,
        featureidkey="properties.NAME",
        projection="mercator",
        #hover_data={"locations": False, "color": False},  # ukrywa te domyślne
        #hover_name=countries,
        )
        fig.update_traces(
        hovertemplate=f'<b>%{{location}}</b><br>{MapValues.PUPK_VALUE.value}: %{{z}}<extra></extra>'
        )

        fig.update_geos(
        #fixedrange=True,
        #fitbounds="locations",  # Dostosuj zoom do danych
        center={"lat": 32.0, "lon": 19.0},  # Środek Polski
        projection_scale=2.5,
        
        #visible=False,          # Ukryj osie
        #showcountries=True,     # Opcjonalnie
        )

        fig.update_layout(
        #autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        #paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)',
        height=800,
        dragmode=False,
        coloraxis_colorbar=dict(
            title="Ilość",
            x=0.02,
            y=0.52,
            xanchor='left',
            yanchor='bottom',
            len=0.2,
            thickness=5,
            #bgcolor='rgba(255,255,255,0.8)',
            #outlinewidth=0
            )
        )
        self.map = fig
class MapCreatorCountries(MapCreator):
    def __init__(self,geo_data):
        super().__init__(geo_data)


class MapCreatorRegions(MapCreator):
    def __init__(self,geo_data):
        
        self.geojson_data = geo_data
        self.indexes = [f["properties"]["NUTS_NAME"] for f in self.geojson_data["features"]]
        self.values = [1 + i % 5 for i in range(len(self.indexes))]
        self.map = self.__draw_map()

    def set_values(self,values):
        self.values = values
        self.map = self.__draw_map()

    def __draw_map(self):
        
        fig = px.choropleth(
            locations=self.indexes,
            geojson=self.geojson_data,
            color=self.values,
            featureidkey="properties.NUTS_NAME",
            projection="mercator",
        )

        fig.update_traces(
            marker_line_color='black',
            marker_line_width=0.4,
            hovertemplate=f'<b>%{{location}}</b><br>{MapValues.PEPR_VALUE.value}: %{{z}}<extra></extra>'
        )

        fig.update_geos(
            center={"lat": 32.0, "lon": 19.0}, 
            projection_scale=5,
        )

        fig.update_layout(
        #autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        #paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)',
        height=800,
        dragmode=False,
        coloraxis_colorbar=dict(
            title="Ilość",
            x=0.02,
            y=0.52,
            xanchor='left',
            yanchor='bottom',
            len=0.2,
            thickness=5,
            #bgcolor='rgba(255,255,255,0.8)',
            #outlinewidth=0
            )
        )

        return fig



