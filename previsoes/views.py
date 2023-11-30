from django.shortcuts import render
from django.http import HttpRequest
from previsoes.models import get_eleicoes_ano, get_cidades_votadas
import plotly.express as px

# Create your views here.
def overview(request):
    eleicoes_ano = get_eleicoes_ano()
    rank_ciades = get_cidades_votadas()

    fig1 = px.bar(
        x=[ str(x[0]) for x in rank_ciades],
        y=[ x[1] for x in rank_ciades],
        title=f"Rank das {len([ x[1] for x in rank_ciades]) } ciadade do PR com mais votos ",
        labels={'y': "Quantidade de Votos", 'x': "Cidade"})


    fig = px.line(
        x=[ str(x[0]) for x in eleicoes_ano],
        y=[ x[1] for x in eleicoes_ano],
        title=f"Quantidade de votos das {len([ x[1] for x in eleicoes_ano]) } últimas eleições presidencias ",
        labels={'y': "Quantidade de Votos", 'x': "Ano"})

    return render(request, "graphs.html", { 'graph_rank': fig1.to_html(), 'graph': fig.to_html() })


def detalhes(request):
    return render(request, "detalhes.html" )