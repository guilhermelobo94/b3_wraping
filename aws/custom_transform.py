def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    from pyspark.sql.functions import datediff, to_date, lit, col, regexp_replace, when
    from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection
    import pytz
    from datetime import datetime

    tz = pytz.timezone('America/Sao_Paulo')
    now_sp = datetime.now(tz).strftime('%Y-%m-%d')

    df = dfc.select(list(dfc.keys())[0]).toDF()

    df_cleaned = df.withColumn(
        "qtde_teorica_cleaned",
        regexp_replace(col("qtde_teorica"), "[^\d]", "").cast("long")
    ).withColumn(
        "participacao_cleaned",
        regexp_replace(col("participacao"), ",", ".").cast("double")
    ).withColumn(
        "participacao_acumulativo_cleaned",
        regexp_replace(col("participacao_acumulativo"), ",", ".").cast("double")
    )

    df_cleaned = df_cleaned.withColumn(
        'data_dados', to_date(col('data'), 'yyyy-MM-dd')
    ).drop('data').withColumn(
        'data_atual', to_date(lit(now_sp), 'yyyy-MM-dd')
    ).withColumn(
        'diferenca_dias', datediff(col('data_atual'), col('data_dados'))
    )

    df_cleaned = df_cleaned.withColumnRenamed('qtde_teorica_cleaned', 'qtde_teorica') \
        .withColumnRenamed('participacao_cleaned', 'participacao') \
        .withColumnRenamed('participacao_acumulativo_cleaned', 'participacao_acumulativo')

    result_dyf = DynamicFrame.fromDF(df_cleaned, glueContext, "result_dyf")

    return DynamicFrameCollection({"CustomTransform0": result_dyf}, glueContext)