from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers="192.168.1.7:9092")
producer.send("testTopic",b'test from python script')
producer.flush()