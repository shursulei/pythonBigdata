from pyspark import SparkConf, SparkContext

# 创建sparkConf，设置spark相关的参数信息
conf = SparkConf().setMaster("local[2]").setAppName("spark0301")
# 创建SparkContext
sc = SparkContext(conf=conf)
# 业务逻辑

data = [1, 2, 3, 4, 5]
disData = sc.parallelize(data)
disData.collect()

# 好的习惯
sc.stop()
