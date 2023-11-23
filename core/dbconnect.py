from pyspark.sql import SparkSession, SQLContext

spark = SparkSession.builder.appName("Trabalho Final Pos") \
.config("spark.jars", "/Users/semicheche/trabalho_final_pos/lib/postgresql-42.2.27.jre7.jar") \
.getOrCreate()

url = "jdbc:postgresql://db-postgresql-nyc3-74721-do-user-9367520-0.c.db.ondigitalocean.com:25060/eleicoes"

properties = {
    "user": "doadmin",
    "password": "AVNS_55SgPxnHeQQCd4Jbhjg",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(url,table="vw_votacao_secao_pr", properties=properties)
print("=====resultado=======")



print(df.head())


# import pandas as pd
# val = pd.DataFrame(df.take(5), columns=df.columns).transpose()

# print(val)