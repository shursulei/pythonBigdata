from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName("Python Spark SQL basic example") \
        .config('spark.some.config,option0', 'some-value') \
        .getOrCreate()

    tablename = "select * from medical.patient_advisory_info where gmt_create>'2020-07-01'"
    a = spark.read.format("jdbc").options(url="jdbc:mysql://basedata-test-in.mysql.rds.aliyuncs.com:3306/user_dataset",
                                          driver="com.mysql.cj.jdbc.Driver", dbtable="medical.patient_advisory_info",
                                          user="sulei",
                                          password="SUww@12343", partitionColumn="id",lowerBound="10000",upperBound="100000",numPartitions=10).load()
    a.write.csv("/data/1.csv",mode="overwrite",sep=",")
    # print(a.cache().head(10));
    print(a.printSchema())
    # print(a.show())
