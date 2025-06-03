import plotly.express as px
import json
import tempfile
import os
from pathlib import Path
from utils.names import MapValues
script_dir = str(Path(__file__).resolve().parent)
# Tworzenie ścieżki do katalogu (np. w folderze projektu lub w folderze użytkownika)
save_path = os.path.join(script_dir+"\\mapa.html")  # zapisuje w katalogu roboczym



class GeoRenderer:

    def __init__(self):

        self.geojson_data=self.__read()
        self.countries = [feature["properties"]["NAME"] for feature in self.geojson_data["features"]]
        self.values = [1] * len(self.countries)  # Możesz tutaj ustawić własne dane
        self.values[self.countries.index('Poland')]=200
        self.fig = self.__mapSetup()
        self.html_content = self.__editHTML(self.fig)
        self.__save()


    def __save(self):
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(self.html_content)

    def __read(self):
        geo = None
        with open(
        script_dir+"\\europa.geojson", "r", encoding="utf-8") as f:
            geo = json.load(f)
        return geo
    
    def __mapSetup(self):
        fig = px.choropleth(
        locations=self.countries,
        geojson=self.geojson_data,
        color=self.values,
        featureidkey="properties.NAME",
        projection="mercator",
        #hover_data={"locations": False, "color": False},  # ukrywa te domyślne
        #hover_name=countries,
        )
        fig.update_traces(
        hovertemplate=f'<b>%{{location}}</b><br>{MapValues.PEPR_VALUE.value}: %{{z}}<extra></extra>'
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
            x=0.02,         # Poziomo prawie maksymalnie z prawej
            y=0.52,         # Pionowo blisko góry
            xanchor='left',
            yanchor='bottom',
            len=0.2,        # Długość (jako ułamek wysokości)
            thickness=5,   # Grubość w px
            #bgcolor='rgba(255,255,255,0.8)',  # tło lekko mleczne
            #outlinewidth=0
            )
        )
        return fig

    def __editHTML(self,fig):
        html_content = fig.to_html(
        full_html=True,
        #include_plotlyjs='cdn', 
        config={'displayModeBar': False}
        )

        html_content = html_content.replace(
            "<head>",
            """<head>
            <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
        }
        .plot-container, .main-svg, .geo {
            width: 100% !important;
            height: 100% !important;
        }
        </style>"""
        )
        return html_content


g = GeoRenderer()
