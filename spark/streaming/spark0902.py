#批处理读取文件系统中的文件
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: spark0902.py <directory>", file=sys.stderr)
        sys.exit(-1)
    sc = SparkContext(appName="spark0902")
    ssc = StreamingContext(sc, 5)

    lines = ssc.textFileStream(sys.argv[1])
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a + b)
    ##out put
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()

    ##file:///xxx.tex.//