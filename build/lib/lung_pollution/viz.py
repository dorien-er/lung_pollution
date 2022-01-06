import plotly.express as px

class Viz():

    def __init__(self, df, counties):
        self.df = df
        self.counties = counties

    def pollutant_map(self, pollutants):
        if pollutants == 'NO_totMean':
            #color_scale = "greys"
            labels = {'NO_totMean': 'NO'}

        elif pollutants == 'NO2_totMean':
            #color_scale = "amp"
            labels = {'NO2_totMean': 'NO2'}

        elif pollutants == 'O3_totMean':
            #color_scale = "amp"
            labels = {'O3_totMean': 'O3'}

        elif pollutants == 'PM2_5_totMean':
            #color_scale = "amp"
            labels = {'PM2_5_totMean': 'PM2.5'}

        fig_pollutant = px.choropleth_mapbox(
            self.df,
            geojson=self.counties,
            locations='county_new',
            featureidkey="properties.NAME_3",
            color=pollutants,
            color_continuous_scale="ylorrd",
            color_continuous_midpoint=None,
            mapbox_style="white-bg",
            zoom=4.5,
            center={
                "lat": 51.312801,
                "lon": 9.481544
            },
            opacity=0.5,
            labels=labels)
        fig_pollutant.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, )
        return fig_pollutant

    def covid_map(self, covids):
        if covids == 'cases_per_100k':
            color_scale = "greys"
            labels = {'cases_per_100k': 'cases per 100k'}
        elif covids == 'deaths_per_100k':
            color_scale = "amp"
            labels = {'deaths_per_100k': 'deaths per 100k'}
        fig_covid = px.choropleth_mapbox(
            self.df,
            geojson=self.counties,
            locations='county_new',
            featureidkey="properties.NAME_3",
            color=covids,
            color_continuous_scale=color_scale,
            color_continuous_midpoint=None,
            mapbox_style="white-bg",
            zoom=4.5,
            center={
                "lat": 51.312801,
                "lon": 9.481544
            },
            opacity=0.5,
            labels=labels
        )
        fig_covid.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig_covid

    def update_graph(self, county_selected):
        dff = self.df[self.df["county_new"] == county_selected]

        height = 280
        width = 350

        template = 'plotly'

        # Graph for pollutant 1 (NO2)
        graph_no2 = px.area(  #### also into plotting script (anything with px)
            dff,
            x='year',
            y='NO2_annualMean',
            title='NO2 (annual mean) [µg/cm3]',
            template=template,
            height=height,
            width=width,
            line_shape='spline',
        ).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title=None, showgrid=True, showticklabels=True),
                        xaxis=dict(title=None, showgrid=False,
                                showticklabels=True))

        graph_no2.update_yaxes(
            showline=False,
            linewidth=0.25,
            matches=None,  #autoscale y axis
            linecolor='gray',
            gridcolor='gray')

        # Graph for pollutant 2 (NO)
        graph_no = px.area(
            dff,
            x='year',
            y='NO_annualMean',
            title='NO (annual mean) [µg/cm3]',
            template=template,
            height=height,
            width=width,
            line_shape='spline',
        ).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title=None, showgrid=True, showticklabels=True),
                        xaxis=dict(title=None, showgrid=False,
                                showticklabels=True))
        graph_no.update_yaxes(showline=False,
                            linewidth=0.25,
                            matches=None,
                            linecolor='gray',
                            gridcolor='gray')

        # Graph for pollutant 3 (O3)
        graph_o3 = px.area(
            dff,
            x='year',
            y='O3_annualMean',
            title='O3 (annual mean) [µg/cm3]',
            template=template,
            height=height,
            width=width,
            line_shape='spline',
        ).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title=None, showgrid=True, showticklabels=True),
                        xaxis=dict(title=None, showgrid=False,
                                showticklabels=True))
        graph_o3.update_yaxes(showline=False,
                            linewidth=0.25,
                            matches=None,
                            linecolor='gray',
                            gridcolor='gray')

        # Graph for pollutant 4 (PM10)
        graph_pm10 = px.area(
            dff,
            x='year',
            y='PM10_annualMean',
            title='PM10 (annual mean) [µg/cm3]',
            template=template,
            height=height,
            width=width,
            line_shape='spline',
        ).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title=None, showgrid=True, showticklabels=True),
                        xaxis=dict(title=None, showgrid=False,
                                showticklabels=True))
        graph_pm10.update_yaxes(showline=False,
                                linewidth=0.25,
                                matches=None,
                                linecolor='gray',
                                gridcolor='gray')

        # Graph for pollutant 5 (PM2.5)
        graph_pm25 = px.area(
            dff,
            x='year',
            y='PM2_5_annualMean',
            title='PM2.5 (annual mean) [µg/cm3]',
            template=template,
            height=height,
            width=width,
            line_shape='spline',
        ).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(title=None, showgrid=True, showticklabels=True),
                        xaxis=dict(title=None, showgrid=False,
                                showticklabels=True))
        graph_pm25.update_yaxes(showline=False,
                                linewidth=0.25,
                                matches=None,
                                linecolor='gray',
                                gridcolor='gray')

        return [graph_no2, graph_no, graph_o3, graph_pm10,
                graph_pm25]  ### use loop instead of repeating code

    if __name__ == '__main__':
        pass
