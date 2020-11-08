
from pykafka import KafkaClient

client = KafkaClient(hosts="127.0.0.1:9092")
print(client.topics['test'])
topic=client.topics['user']
consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print(message.offset, message.value)