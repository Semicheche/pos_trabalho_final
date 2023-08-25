# pos_trabalho_final

### Trabalhho de eaanalise de dados baseano nas Eleicoes do Ano de 2022
 Histórico totalização Presidente - Votação nominal/partido por município e zona - Detalhe da apuração por município e zona/seção eleitoral - Votação por seção eleitoral

[**PR - Votação por seção eleitoral - 2022**](https://dadosabertos.tse.jus.br/dataset/resultados-2022/resource/ac7bb6a5-68e4-4852-a690-dd2b526c92ee)

### Obrigatorio
- Python 3.11
- Download da base da dados non link acima

### Configuracao Linux/OSX
- Faca o clone do repositorio
```
 $ git clone link
```
-  acesse o repositrio
```
$ cd trabalho_final_pos
```
- crie o ambiente virtual
```
$ python3.11 -m venv env
```
- ative o ambiente virtual
```
    $ source env/bin/activate
```
- verifique se o ambiente foi ativado
```
(env) $ trabalho_final_pos
```
- extraia a base de dados e mova a pasta para a raiz do projeto
```
**Dowloads**$ unzip votacao_secao_2022_PR.zip ~/<path>/trabalho_final_pos
```
- instale as dependencias do projeto
```
$ pip install -r requirements.txt
```
### Pronto agora e so rodar o Projeto
- na raiz do projeto execute
```
$ solara run app
```
- pronto basta acessar a ulr `http://localhost:8765/`