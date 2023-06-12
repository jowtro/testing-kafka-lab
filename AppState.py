# Create a Singleton metaclass to store the producer
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AppState(metaclass=Singleton):
    def __init__(self):
        self.producer: AIOKafkaProducer = None
        self.consumer: AIOKafkaConsumer = None
