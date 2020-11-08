'''nc -lk 9999`'''
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
if __name__ == "__main__":
    #if len(sys.argv) != 3:
      #  print("Usage: network_wordcount.py <hostname> <port>", file=sys.stderr)
      #  sys.exit(-1)
    sc = SparkContext(appName="spark0901")
    ssc = StreamingContext(sc, 5)

    lines = ssc.socketTextStream("", 9999)
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a + b)
    ##out put
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()