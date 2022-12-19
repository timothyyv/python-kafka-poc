from random import randint
from typing import Set, Any
from fastapi import FastAPI, Depends
from kafka import TopicPartition
from dotenv import load_dotenv
from aggregator_functions import Aggregator

import uvicorn
import aiokafka
import asyncio
import json
import logging
import os

load_dotenv()
app = FastAPI()

# set up global variables
consumer_task = None
consumer = None
_state = 0


# env variables
KAFKA_TOPICS = os.environ.get('KAFKA_TOPICS')
KAFKA_CONSUMER_GROUP_PREFIX = os.environ.get('KAFKA_CONSUMER_GROUP_PREFIX', 'group')
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    log.info('Initializing API ...')
    agg = Aggregator()
    agg.sum()
    # await init()
    # await consume()


@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')
    consumer_task.cancel()
    await consumer.stop()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/state")
async def state():
    return {"state": _state}


# initialize the kafka consumer after server crash or on first start up
async def init():
    # get event loop
    # loop = asyncio.get_event_loop()
    global consumer
    # generate a randomized group id for 
    group_id = f'{KAFKA_CONSUMER_GROUP_PREFIX}-{randint(0, 10000)}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_TOPICS}, group_id {group_id}'
        f'and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    # set up the consumer
    consumer = aiokafka.AIOKafkaConsumer(KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, 
        group_id=group_id)

    # connect to kafka cluster and add consumer to group
    await consumer.start()

    # get set of partitions assigned to this consumer
    partitions: Set[TopicPartition] = consumer.assignment()
    no_partitions = len(partitions)

    if no_partitions != 1:
        log.warning(f'Found {no_partitions} partitions for topics {KAFKA_TOPICS}, expecting'
            f'only one, remaining partitions will be ignored!')
    
    for topic_partition in partitions:
        # get offset of the last available message 
        end_offset_dict = await consumer.end_offsets([topic_partition])
        end_offset = end_offset_dict[topic_partition]

        # check if offset value is 0, this denotes that there are no messages
        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPICS}) has no messages (log_end_offset: ' 
                f'{end_offset}), skipping initialization ...')
            return
        
        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset - 1}')
        consumer.seek(topic_partition, end_offset - 1)
        msg = await consumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')

        # update API state
        _update_state(msg)
        return


# create a coroutine task for execution
async def consume():
    global consumer_task
    consumer_task = asyncio.create_task(send_consumer_message(consumer))


# consume messages after init
async def send_consumer_message(consumer):
    try:
        # cosnume messages
        async for msg in consumer:
            log.info(f'Consumed msg: {msg}')
            _update_state(msg)
    finally:
        log.warning('Stopping consumer')
        await consumer.stop()


def _update_state(message: Any) -> None:
    value = json.loads(message.value)
    global _state
    _state = value['state']



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
