import asyncio
import json
import os
import signal
from aiokafka import AIOKafkaConsumer
from AppState import AppState

from config import BOOTSTRAP_SERVERS, TOPIC


async def consume_messages(bootstrap_servers, topic):
    # Create a Kafka consumer
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="my_consumer_group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    AppState().consumer = consumer
    # Start the consumer
    await AppState().consumer.start()

    try:
        # Consume messages
        async for msg in consumer:
            print(f"Received msg: {msg.value}")

    finally:
        # Stop the consumer
        await AppState().consumer.stop()


def handler(signum=None, frame=None):
    """Handler to stop the script gracefully"""

    # Try to stop the producer
    if AppState().consumer is not None:
        print("Stopping consumer")
        loop = asyncio.get_event_loop()
        loop.create_task(AppState().consumer.stop())

    os.popen(f"kill -9 {os.getpid()}")  # or signal.SIGKILL


if __name__ == "__main__":
    # Load each signal to the handler function for graceful script termination
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]:
        signal.signal(sig, handler)
    # Run the event loop to consume messages
    asyncio.run(consume_messages(BOOTSTRAP_SERVERS, TOPIC))
