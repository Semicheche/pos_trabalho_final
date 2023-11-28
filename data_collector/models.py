from django.db import models

class Pais(models.Model):
    codigo = models.CharField(max_length=4, primary_key=True)
    sigla = models.CharField(max_length=2)
    descricao = models.CharField(max_length=30)
    ddi = models.CharField(max_length=2, blank=True, null=True)

class Estado(models.Model):
    codigo = models.CharField(max_length=2, primary_key=True)
    descricao = models.CharField(max_length=30)
    sigla = models.CharField(max_length=2)
    codigo_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='codigo_pais')
    codigo_unico = models.CharField(max_length=5)

class Cidade(models.Model):
    codigo = models.CharField(max_length=7, primary_key=True)
    descricao = models.CharField(max_length=30)
    latitude = models.TextField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    cd_municipio = models.IntegerField(blank=True, null=True)
    codigo_estado = models.ForeignKey(Estado, on_delete=models.CASCADE, db_column='codigo_estado')
    class Meta:
        indexes = [
            models.Index(fields=['cd_municipio'], name='idx_cd_municipio_cidade'),
        ]

class VotacaoSecao(models.Model):
    DT_GERACAO = models.DateField()
    HH_GERACAO = models.CharField(max_length=8)
    ANO_ELEICAO = models.IntegerField()
    CD_TIPO_ELEICAO = models.IntegerField()
    NM_TIPO_ELEICAO = models.CharField(max_length=20)
    NR_TURNO = models.IntegerField()
    CD_ELEICAO = models.IntegerField()
    DS_ELEICAO = models.CharField(max_length=50)
    DT_ELEICAO = models.DateField()
    TP_ABRANGENCIA = models.CharField(max_length=1)
    SG_UF = models.CharField(max_length=2)
    SG_UE = models.CharField(max_length=10)
    NM_UE = models.CharField(max_length=50)
    CD_MUNICIPIO = models.IntegerField()
    NM_MUNICIPIO = models.CharField(max_length=50)
    NR_ZONA = models.IntegerField()
    NR_SECAO = models.IntegerField()
    CD_CARGO = models.IntegerField()
    DS_CARGO = models.CharField(max_length=20)
    NR_VOTAVEL = models.IntegerField()
    NM_VOTAVEL = models.CharField(max_length=70)
    QT_VOTOS = models.IntegerField()
    NR_LOCAL_VOTACAO = models.IntegerField()
    NM_MUNICIPIO_2 = models.CharField(max_length=50)
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['ano_eleicao'], name='idx_ano'),
            models.Index(fields=['sg_uf'], name='idx_sg_uf'),
            models.Index(fields=['cd_municipio'], name='idx_cd_municipio'),
            models.Index(fields=['nm_municipio'], name='idx_nm_municipio'),
        ]

class VotacaoSecao1998PR(VotacaoSecao):
    pass

class VotacaoSecao2002PR(VotacaoSecao):
    pass

class VotacaoSecao2006PR(VotacaoSecao):
    pass

class VotacaoSecao2010PR(VotacaoSecao):
    pass

class VotacaoSecao2014PR(VotacaoSecao):
    pass

class VotacaoSecao2018PR(VotacaoSecao):
    pass

class VotacaoSecao2022PR(VotacaoSecao):
    pass
