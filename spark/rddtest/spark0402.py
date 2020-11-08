import sys
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:wordcount <input> <output>", file=sys.stderr)
        sys.exit(-1)
    conf = SparkConf().setMaster("local[2]").setAppName("spark0401")
    sc = SparkContext(conf=conf)
    #输出到控制台中
    def printResult():
        counts = sc.textFile(sys.argv[1]).flatMap(lambda line: line.split("\t")).map(lambda x: (x, 1)).reduceByKey(
            lambda a, b: a + b)
        output = counts.collect()
        for (word, count) in output:
            print("%s: %i" % (word, count))
    #输出到文件系统中
    def saveFile():
         sc.textFile(sys.argv[1]).flatMap(lambda line: line.split("\t")).map(lambda x: (x, 1)).reduceByKey(
            lambda a, b: a + b).saveAsTextFile(sys.argv[2])
    sc.stop
