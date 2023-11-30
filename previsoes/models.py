from django.db import models
from django.db import connection

# Create your models here.
def get_eleicoes_ano():
    cursor = connection.cursor()
    cursor.execute(''' SELECT
                    ano_eleicao,
                    COUNT (ano_eleicao) AS qtde
                FROM
                    vw_votacao_secao_pr
                GROUP BY
                    ano_eleicao
                ORDER BY
                    ano_eleicao;''')
    return cursor.fetchall()

def get_cidades_votadas():
    cursor = connection.cursor()
    cursor.execute(''' SELECT
                        C.descricao AS cidade,
                        COUNT (VW.cd_municipio)	AS qtde_votos
                    FROM
                        vw_votacao_secao_pr VW
                    INNER JOIN
                        cidade C ON C.cd_municipio = VW.cd_municipio
                    GROUP BY
                        C.descricao
                    ORDER BY
                        2 DESC
                    LIMIT 10;''')
    return cursor.fetchall()
