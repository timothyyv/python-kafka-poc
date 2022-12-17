from aiokafka import AIOKafkaProducer
from kafka import KafkaProducer
from random import randint
import asyncio
import json
import os
import os


KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')

async def kafka_producer(data):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        enable_idempotence=True)
    await producer.start()

    try:
        print(f'Sending message with value: {data}')
        value_json = json.dumps(data).encode('utf-8')
        await producer.send_and_wait(KAFKA_TOPIC, value_json)
        print(f"Done sending...{data['account_number']}")
    finally:
        # wait for all pending messages to be delivered or expire
        await producer.stop()
