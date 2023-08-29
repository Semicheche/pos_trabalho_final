from typing import Optional, cast

import pandas as pd
import datetime
import requests

import solara
import solara.express as solara_px  # similar to plotly express, but comes with cross filters
import solara.lab
from solara.components.columns import Columns
from solara.components.file_drop import FileDrop
import geopandas as gpd
from ipywidgets import HTML

#maps
import ipyleaflet
from ipyleaflet import Map, LayersControl, Marker, Popup, Heatmap
# # from . import SharedComponent

# #github_url = solara.util.github_url(__file__)
# #try:
#     # fails on pyodide

# # except:  # noqa
# #     df_sample = None
# app_state = solara.reactive(0)

datasets = {
        "votacao": {
            "type":"csv",
            "url": "/Users/semicheche/trabalho_final_pos/votacao_secao_2022_PR/votacao_secao_2022_PR.csv",
            "sep": ";",
            "encoding": "Latin1",
            "function": "base_csv"
        },
        # "eleicoes": {
        #             "type": "csv",
        #             "url": "/Users/semicheche/trabalho_final_pos/bweb_1t_PR_051020221321/bweb_1t_PR_051020221321.csv",
        #             "sep": ";",
        #             "encoding": "Latin1"},
        #             "function": "base_csv"

        "municipios": {
            "type": "json",
            "url": "/Users/semicheche/trabalho_final_pos/municipio.json",
            "sep": "",
            "encoding": "",
            "function": "load_municipio"
        },
        "uf": {
            "type": "json",
            "url": "/Users/semicheche/trabalho_final_pos/uf.json",
            "sep": "",
            "encoding": "",
            "function": "base_csv"
        }
    }

class State:
    size_max = solara.reactive(40.0)
    size = solara.reactive(cast(Optional[str], None))
    color = solara.reactive(cast(Optional[str], None))
    x = solara.reactive(cast(Optional[str], None))
    y = solara.reactive(cast(Optional[str], None))
    tipo = solara.reactive(cast(Optional[str], None))
    logx = solara.reactive(False)
    logy = solara.reactive(False)
    df = solara.reactive(cast(Optional[pd.DataFrame], None))
    df_municipios = solara.reactive(cast(Optional[pd.DataFrame], None))
    df1 = solara.reactive(cast(Optional[pd.DataFrame], None))
    columns = solara.reactive(cast(Optional[str], []))
    cargo = solara.reactive(cast(Optional[str], None))

    dh_ini = solara.reactive(cast(Optional[str], None))
    dh_tempo = solara.reactive(cast(Optional[str], None))
    ###
    nominatim_data = solara.reactive([])

    msg_load_base = solara.reactive(cast(Optional[str], None))
    msg = solara.reactive(cast(Optional[str], None))

    colunas = solara.reactive(cast(Optional[str], None))

    municipio = solara.reactive(cast(Optional[str], None))
    nome_municipio = solara.reactive(cast(Optional[str], None))
    id_municipio = solara.reactive(cast(Optional[str], None))
    info_municipio = solara.reactive(cast(Optional[str], None))
    candidato = solara.reactive(cast(Optional[str], None))
    result = solara.reactive(cast(Optional[str], None))

    get_positions = solara.reactive(cast(Optional[bool], False))
    check = solara.reactive(False)

    municipios = solara.reactive(cast(Optional[str], []))

    cargo_candidato = solara.reactive(cast(Optional[str], None))
    candidato_por_municipio = solara.reactive(cast(Optional[str], None))
    
    IBGE_info = solara.reactive(cast({}, {}))

    @staticmethod
    def set_col(df):
        return solara.reactive([list(df.columns)[0]])

    @staticmethod
    def load_sample():
        State.x.value = str("gdpPercap")
        State.y.value = str("lifeExp")
        State.size.value = str("pop")
        State.color.value = str("continent")
        State.logx.value = True
        State.df.value = df_sample

    @staticmethod
    def load_from_file(file):
        df = pd.read_csv(file["file_obj"])
        State.x.value = str(df.columns[0])
        State.y.value = str(df.columns[1])
        State.size.value = str(df.columns[2])
        State.color.value = str(df.columns[3])
        State.df.value = df

    @staticmethod
    def reset():
        State.df.value = None

class DataSet():
    def load_dataframe():
        df= None
        df1 = None
        df2 = None
        for k, v in datasets.items():
            print("============")
            if v['type'] == 'csv':
               print(f"Carregando o Csv dos {k}" )
               df = pd.read_csv(v['url'], sep=v['sep'], encoding=v['encoding'])
            if v['type'] == 'json':
                if k == "municipios":
                    print(f"Carregando o dados {k}" )
                    df1 = gpd.read_file(v['url'])
                    df1['name'] = [str(name).upper() for name in df1['name']]
                # if k == "uf":
                #     print(f"Carregando o dados {k}" )
                #     df2 = gpd.read_file(v['url'])
                #     print(df2.head(4))


        print(f"Mescla o dados Municipios e eleicoes" )
        gdf = df1.merge(df, left_on='name', right_on='NM_MUNICIPIO')
       # gdf = gdf.merge(df2, left_on='SG_UF', right_on='UF_05')

        return gdf

    def load_data(uf=None):
        df= None
        for k, v in datasets.items():
            if v['type'] == 'csv':
               print(f"Carregando o Csv dos {k}")
               State.msg = f"Carregando o Csv dos {k}"
               df = pd.read_csv(v['url'], sep=v['sep'], encoding=v['encoding'])

        return df

def load_municipio():
    municipio_data = gpd.read_file("/Users/semicheche/trabalho_final_pos/municipio.json")
    
    get_centroids(municipio_data)

    municipio_data['IBGE_INFO'] = State.IBGE_info.value.values()
    State.df_municipios.value = municipio_data

def get_ibge_info():
    info_municipio = requests.get(f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{State.id_municipio}/metadados")
    State.info_municipio.value = info_municipio.json()

def get_ibge_by_id(id_municipio):

    if id_municipio not in State.IBGE_info.value.keys():
        print(id_municipio)
        info_municipio = requests.get(f"https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{id_municipio}/metadados")
        State.IBGE_info.value.setdefault(id_municipio,  info_municipio.json()[0])

def line():
        return solara.Markdown("___")

def activate():

    State.get_positions = True if not State.get_positions else False
def reset_select():
    State.municipios.value = []

def generate_graph():
    df1 = State.df1

    dt = df1[df1["NM_MUNICIPIO"] == State.municipio.value]
    dt = dt[dt["NM_VOTAVEL"] == State.candidato.value]
    res = dt.sum()
    State.result.value = res["QT_VOTOS"]

def base_mesclada():
    State.df.value = DataSet.load_dataframe()

def base_csv():
    State.dh_ini = datetime.datetime.now()
    State.df.value = DataSet.load_data()
    State.dh_tempo = datetime.datetime.now() - State.dh_ini
    State.msg_load_base = f"DADOS CARREGADOS: duracao: {State.dh_tempo}"

@solara.component
def IncrementButton():

    solara.Select("Column x", values=columns, value=State.x)
    solara.Button("Load Dados Eleicoes", on_click=DataSet.load_dataframe)
    solara.Button("UF", on_click=DataSet.load_uf)
    solara.Button("Municipios", on_click=DataSet.load_municipio)

@solara.component
def Home():
    df = None

    with solara.Sidebar():
        with solara.Card("CLIQUE PARA CARREGAR A BASE DE DADOS:", margin=0, elevation=0):
            with solara.Column():
                with solara.Row():
                    for k, v in datasets.items():
                        if k == 'votacao':
                            solara.Button(f"Dados {k}", color="primary", text=True, outlined=True, on_click=globals()[v['function']])
                    
                with solara.Row():
                    for k, v in datasets.items():
                        if k == 'municipios':
                            solara.Button(f"Dados {k}", color="primary", text=True, outlined=True, on_click=globals()[v['function']])
                        #solara.Button("Base Dados CSV", color="primary", text=True, outlined=False, on_click=base_csv)
                        #solara.Button("Base Dados CSV", color="primary", text=True, outlined=False, on_click=base_csv)

                    df = State.df.value


    if df.__class__ != None.__class__:
        if isinstance(State.dh_tempo, datetime.timedelta):
            with solara.Row():
                solara.Success(State.msg_load_base)
        with solara.Card("DETALHES DA BASE DE DADOS:", margin=0, elevation=0):
            solara.Markdown("""
                            Histórico totalização Presidente - Votação nominal/partido por município e zona - Detalhe da apuração por município e zona/seção eleitoral - Votação por seção eleitoral...

                            [**PR - Votação por seção eleitoral - 2022**](https://dadosabertos.tse.jus.br/dataset/resultados-2022/resource/ac7bb6a5-68e4-4852-a690-dd2b526c92ee)
                            """)
            line()
            solara.Markdown(f"### {len(list(df.columns))} COLUNAS ")
            with solara.ColumnsResponsive(3,large=2):
                for i in list(df.columns):
                    with solara.Column():
                        solara.Markdown(f"##### {i}")
            with solara.Column():
                line()
            with solara.ColumnsResponsive(2,large=2):
                solara.Markdown("### SHAPE DOS DATAFREME")

                solara.Markdown(f"##  :{df.shape[0]}x{df.shape[1]}")
    #             with solara.Column():
    #                 with solara.Row():
    #                     solara.Select("Column x", values=list(df.columns), value=State.x)
    #                     solara.Select("Column y", values=list(df.columns), value=State.y)
    #                     #solara.Select("SELECIONE O TIPO DE DADOS:", values=list(df['DS_CARGO_PERGUNTA']), value=State.tipo)
        line()
        df1 = None
        solara.DataFrame(df.head())
        solara.Markdown("# DataFrame por Colunas Selecionadas")
        line()
        State.set_col(df)
        solara.SelectMultiple("COLUNAS",values=State.colunas, all_values=list(df.columns))
        if State.colunas.value:
            solara.Markdown(f"{', '.join(State.colunas.value)}")
            solara.DataFrame(df[State.colunas.value])
            df1 = df[State.colunas.value]
            State.df1 = df1

        else:
            solara.DataFrame(df)
        with solara.Card(f"Filltro por candidatos", margin=0, elevation=0):
            with solara.Column():
                with solara.Row():
                    if df1.__class__  != None.__class__:
                        if "NM_MUNICIPIO" in df1.columns:
                            solara.Select("Municipio", list(df1["NM_MUNICIPIO"].unique()), value=State.municipio)
                        if "NM_VOTAVEL" in df1.columns:
                            solara.Select("Candidato", list(df1["NM_VOTAVEL"].unique()), value=State.candidato)
                        if "DS_LOCAL_VOTACAO_ENDERECO" in df1.columns:
                            solara.Select("Endereco", list(df1["DS_LOCAL_VOTACAO_ENDERECO"].unique()), value=State.candidato)
                        if "NM_MUNICIPIO" in df1.columns and "NM_VOTAVEL" in df1.columns:
                            solara.Button("Carregar", color="primary", text=True, outlined=False, on_click=generate_graph)
                            if "DS_LOCAL_VOTACAO_ENDERECO" in df1.columns:
                                dados_end = {
                                "cidade": df1[(df1['NM_MUNICIPIO'] == State.municipio.value) & (df1['NM_VOTAVEL'] == State.candidato.value)]["NM_MUNICIPIO"],
                                "endereco": df1[(df1['NM_MUNICIPIO'] == State.municipio.value) & (df1['NM_VOTAVEL'] == State.candidato.value)]['DS_LOCAL_VOTACAO_ENDERECO'],
                                "nome": df1[(df1['NM_MUNICIPIO'] == State.municipio.value) & (df1['NM_VOTAVEL'] == State.candidato.value)]['NM_LOCAL_VOTACAO'],
                                "qt_votos": df1[(df1['NM_MUNICIPIO'] == State.municipio.value) & (df1['NM_VOTAVEL'] == State.candidato.value)].groupby('NM_LOCAL_VOTACAO').sum(['QT_VOTOS'])
                                }

                                solara.Button("Pegar ponto de LatLng", color="primary", text=True, outlined=False, on_click=activate)
                                if State.get_positions:
                                    get_location(dados_end)

        with solara.Card(f"Plot dos Geodados", margin=0, elevation=0):
            municipios = None
            with solara.ColumnsResponsive(2,large=12):
                url = ipyleaflet.basemaps.OpenStreetMap.Mapnik["url"]
                layers = [ipyleaflet.TileLayer.element(url=url)]
                if hasDataFrame(State.df_municipios.value):
                    municipios = State.df_municipios.value
                    solara.Markdown(f""" # TOTAL DE {len(municipios)} MMUNICIPIOS
                                """)
                if hasDataFrame(municipios):
                    geo_data = ipyleaflet.GeoData(geo_dataframe = municipios,
                            style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.05, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.6},
                            hover_style={'fillColor': 'red' , 'fillOpacity': 0.2},
                            name = 'Municipio')
                    layers.append(geo_data)


                if len(State.nominatim_data.value) > 0:
                    for dt_latlon in State.nominatim_data.value:
                        for  k, v in dt_latlon.items():
                            marker = ipyleaflet.Marker.element(location=(v['lat'], v['lon']), draggable=False, title=f"{v['nome']} \nVotos: {v.get('qtd')}")

                            layers.append(marker)

                map = Map.element(
                                center=(-24.2393431,-50.88778),
                                zoom=7,
                                layers=layers)
    else:
        solara.Info("Carregue a base de dados")

def get_centroids(dataframe=None,):
    for data in dataframe['id']:
        get_ibge_by_id(data)


def hasDataFrame(datafrfame):
    return datafrfame.__class__ != None.__class__

def get_location(dados_end):
    if len(State.nominatim_data.value) == 0:
        cidade = []
        street =  []

        cidade =f"city={State.municipio.value}"
        dados_latlon = {}

        for i, v in enumerate(dados_end['nome']):

            dados_latlon.setdefault(v, { "nome": v,
                                        "qtd": dados_end['qt_votos'].loc[v]['QT_VOTOS'],
                                        "lat": 0,
                                        "lon": 0
                                        })
            end =  dados_end['endereco'].to_numpy()[i].split(",")
            end.reverse()
            s = f"street={dados_end['endereco'].to_numpy()[i].strip().replace(' ', '+')}"
            #s = f"street={''.join(end).strip().replace(' ', '+')}"
            street.append(s)

            if v not in [ v['nome'] for v in State.nominatim_data.value]:

                url = f"https://nominatim.openstreetmap.org/?{s}&{cidade}&format=json&limit=1"
                data = requests.get(url)

                if isinstance(data.json(), list):
                    if len(data.json()) > 0:
                        dados_latlon[v]["lat"] = data.json()[0]['lat']
                        dados_latlon[v]["lon"] = data.json()[0]['lon']

        State.nominatim_data.value.append(dados_latlon)


@solara.component
def FilterData():
    solara.Markdown("DEtalhes do DATAFRAME")
    State.df.describe()

@solara.component
def Candidato():
    solara.Markdown("MUNICIPIO")
    mun = State.df_municipios.value
    df1 = State.df.value
    df3 = None
    if hasDataFrame(mun) and hasDataFrame(df1):
        mun['municipio'] = [ m.upper() for m in mun['name']]
        df2 = mun.merge(df1, right_on='NM_MUNICIPIO', left_on='municipio')

        with solara.ColumnsResponsive(2, large=6):
            solara.Select('Cargo', values=list(df2['DS_CARGO'].unique()), value=State.cargo_candidato)
            if State.cargo_candidato.value:
                solara.Select('Candidadato', values=list(df2[df2['DS_CARGO'] == State.cargo_candidato.value]['NM_VOTAVEL'].unique()), value=State.candidato_por_municipio)

            df3 = df2[(df2['DS_CARGO'] == State.cargo_candidato.value) & (df2['NM_VOTAVEL'] == State.candidato_por_municipio.value)]

            solara.Markdown(f""" # {State.candidato_por_municipio.value}""")
            solara.Markdown(f""" ## TOTAL DE VOTOS {df3['QT_VOTOS'].sum()}""")
            solara.Markdown(f""" ## QUANTIDADE DE MUNICIPIOS QUE VOTOU {len(df3['NM_MUNICIPIO'].unique())} de {len(df1['NM_MUNICIPIO'].unique())}""")

        with solara.ColumnsResponsive(2, large=6):
            with solara.Column():
                if hasDataFrame(df3):
                    url = ipyleaflet.basemaps.OpenStreetMap.Mapnik["url"]
                    layers_candidato = [ipyleaflet.TileLayer.element(url=url)]
                    df4 = mun
                    if hasDataFrame(df4):
                        df4 = df4[df4['municipio'].isin(df3['NM_MUNICIPIO'].unique())]
                        geo_data = ipyleaflet.GeoData(geo_dataframe = df4,
                                style={'color': 'black', 'fillColor': '#3366cc', 'opacity':0.1, 'weight':1.9, 'dashArray':'2', 'fillOpacity':0.2},
                                hover_style={'fillColor': 'red' , 'fillOpacity': 0.2},
                                name = 'nome')
                        layers_candidato.append(geo_data)
                      
                        map = Map.element(
                                        center=(-24.2393431,-50.88778),
                                        zoom=7,
                                        layers=layers_candidato)
            with solara.Column():
   
                locations = [ (v['centroide']['latitude'], v['centroide']['longitude']) for v in df3['IBGE_INFO']]
                url = ipyleaflet.basemaps.OpenStreetMap.Mapnik["url"]
                layers_mapa_calor = [ipyleaflet.TileLayer.element(url=url)]
                heatmap = Heatmap(
                    locations=locations,
                    radius=25
                )
                layers_mapa_calor.append(heatmap)
                map = Map.element(
                                center=(-24.2393431,-50.88778),
                                zoom=7,
                                layers=layers_mapa_calor)
@solara.component
def About():
    with solara.Card("", margin=0, elevation=0):
        mun = State.df_municipios.value
        df1 = State.df.value
        df2 = None
        if hasDataFrame(mun) and hasDataFrame(df1) :
            solara.Success("Dados de Municipios e Votacao")
            with solara.ColumnsResponsive(6, large=6):
                solara.SelectMultiple("Municipio", all_values=list(mun["name"]), values=State.municipios)
                solara.Button("Limpar Selecao", on_click=reset_select)
                if len(State.municipios.value) > 0:
                    if isinstance(State.municipios.value, list):
                        df2 = df1[df1['NM_MUNICIPIO'].isin([ mun.upper() for mun in State.municipios.value])]

                        with solara.ColumnsResponsive(8, large=8):
                            if hasDataFrame(df2):
                                solara.Markdown(f""" ## TOTAL DE VOTOS:
                                                    {df2['QT_VOTOS'].sum()} """)
            if len(State.municipios.value) > 0:
                with solara.ColumnsResponsive(2, large=6):
                    if hasDataFrame(df2):
                        with solara.Column():
                            solara.Markdown("# GOVERNADOR ")
                            df4 = df2[df2['DS_CARGO'] == "GOVERNADOR"]
                            solara_px.pie(df4, names=df4['NM_VOTAVEL'], values=df4['QT_VOTOS'],height=700 )
                        with solara.Column():
                            solara.Markdown("# SENADOR ")
                            df5 = df2[df2['DS_CARGO'] == "SENADOR"]
                            solara_px.pie(df5, names=df5['NM_VOTAVEL'], values=df5['QT_VOTOS'],height=700 )
                with solara.Column():
                    if hasDataFrame(df2):
                        solara.Select("Cargo", values=list(df2['DS_CARGO'].unique()), value=State.cargo)
                        if State.cargo.value:
                            df3 = df2[df2['DS_CARGO'] == State.cargo.value]
                            solara_px.histogram(df3, y=df3['NM_VOTAVEL'], x=df3['QT_VOTOS'],height=900 )

routes = [
    solara.Route(path="/", component=Home, label="DADOS ELEITORAIS PR 2022"),
    solara.Route(path="MUNICIPIOS", component=About, label="MUNICIPIOS"),
    solara.Route(path="CANDIDATOS", component=Candidato, label="CANDIDATOS"),
]