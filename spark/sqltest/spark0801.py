
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import *
def basic(spark):
    df=spark.read.json("file:D://shursulei//software//spark-2.4.3-bin-hadoop2.7//examples//src//main//resources")
    df.show()
    df.printSchema()
    df.select("name").show()
    df.select(df['name'],df['age']+1).show()
    df.filter(df['age']>21).show()
    df.createOrReplaceTempView("people")#注册临时表
    sqlDF=spark.sql("SELECT * FROM people")
    sqlDF.show()
    #RDD转成DataFrame
def schema_inference_example(spark):
    sc = spark.sparkContext

    # Load a text file and convert each line to a Row.
    lines = sc.textFile("examples/src/main/resources/people.txt")
    parts = lines.map(lambda l: l.split(","))
    people = parts.map(lambda p: Row(name=p[0], age=int(p[1])))
    schemaPeople = spark.createDataFrame(people)
    schemaPeople.createOrReplaceTempView("people")
    teenagers = spark.sql("SELECT name FROM people WHERE age >= 13 AND age <= 19")

    teenNames = teenagers.rdd.map(lambda p: "Name: " + p.name).collect()
    for name in teenNames:
        print(name)
def programmatic_schema_example(spark):
    sc = spark.sparkContext

    # Load a text file and convert each line to a Row.
    lines = sc.textFile("examples/src/main/resources/people.txt")
    parts = lines.map(lambda l: l.split(","))
    # Each line is converted to a tuple.
    people = parts.map(lambda p: (p[0], p[1].strip()))

    # The schema is encoded in a string.
    schemaString = "name age"

    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
    schema = StructType(fields)
    # Apply the schema to the RDD.
    schemaPeople = spark.createDataFrame(people, schema)
    # Creates a temporary view using the DataFrame
    schemaPeople.createOrReplaceTempView("people")
    # SQL can be run over DataFrames that have been registered as a table.
    results = spark.sql("SELECT name FROM people")

    results.show()
    # +-------+
    # |   name|
    # +-------+
    # |Michael|
    # |   Andy|
    # | Justin|
    # +-------+
    results.rdd.collect()
if __name__ == '__main__':
    #创建
    spark=SparkSession.builder.appName("spark0801").getOrCreate()
    #业务逻辑处理
    basic(spark)


    #关闭
    spark.stop
