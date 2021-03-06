from kafka import KafkaConsumer, KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='localhost:9092',
value_serializer=lambda v: json.dumps(v).encode('utf-8'))        

def send_message(topic,mess):
	producer.send(topic, mess)
	producer.flush()
