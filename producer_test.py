import asyncio
import json
import os
import signal
from aiokafka import AIOKafkaProducer
from AppState import AppState

from config import BOOTSTRAP_SERVERS, TOPIC


async def send_message(bootstrap_servers, topic, message):
    # Create a Kafka producer
    producer = AIOKafkaProducer(
        bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    # Store the producer in the AppState singleton
    AppState().producer = producer

    # Start the producer
    await producer.start()
    try:
        while True:
            # Produce a JSON message
            await producer.send_and_wait(topic, message)
            print(f"Message sent successfully to: {topic}")
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        await producer.stop()
        print("Producer stopped")
    finally:
        # Stop the producer
        await producer.stop()


def handler(signum=None, frame=None):
    """Handler to stop the script gracefully"""

    # Try to stop the producer
    if AppState().producer is not None:
        print("Stopping producer")
        loop = asyncio.get_event_loop()
        loop.create_task(AppState().producer.stop())

    os.popen(f"kill -9 {os.getpid()}")  # or signal.SIGKILL


if __name__ == "__main__":
    # Load each signal to the handler function for graceful script termination
    for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]:
        signal.signal(sig, handler)

    # Set the message to send as a JSON object
    message = {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}

    asyncio.run(send_message(BOOTSTRAP_SERVERS, TOPIC, message))
