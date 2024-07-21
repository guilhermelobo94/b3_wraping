def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    from pyspark.sql.functions import datediff, to_date, lit, col, regexp_replace
    from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
    import pytz
    from datetime import datetime

    tz = pytz.timezone('America/Sao_Paulo')
    now_sp = datetime.now(tz).strftime('%Y-%m-%d')

    df = dfc.select(list(dfc.keys())[0]).toDF()

    df_cleaned = df.withColumn("qtde_teorica",
                               regexp_replace(col("qtde_teorica"), "\.", "")
                               ).withColumn("qtde_teorica",
                                            col("qtde_teorica").cast("int")
                                            ).withColumn("participacao",
                                                         regexp_replace(col("participacao"), ",", ".").cast("double")
                                                         ).withColumn("participacao_acumulativo",
                                                                      regexp_replace(col("participacao_acumulativo"),
                                                                                     ",",
                                                                                     ".").cast("double")
                                                                      )

    df_cleaned = df_cleaned.withColumn('data_dados', to_date(col('data'), 'yyyy-MM-dd')).drop('data')
    df_cleaned = df_cleaned.withColumn('data_atual', to_date(lit(now_sp), 'yyyy-MM-dd'))
    df_cleaned = df_cleaned.withColumn('diferenca_dias', datediff(df_cleaned['data_atual'], df_cleaned['data_dados']))

    result_dyf = DynamicFrame.fromDF(df_cleaned, glueContext, "result_dyf")

    return DynamicFrameCollection({"CustomTransform0": result_dyf}, glueContext)