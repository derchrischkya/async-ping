import gnsq
import os

class NSQReceiver:
    def __init__(self, topic: str, channel: str):
        self.consumer = gnsq.Consumer(topic, channel, f"{os.getenv('MESSAGE_BROKER_HOST')}:{os.getenv('MESSAGE_BROKER_PORT')}")
        self.consumer.on_message.connect(self.handler)

    def start(self):
        # Start the consumer to begin processing messages
        self.consumer.start()

    def handler(self, consumer, message):
        # This function will be triggered for each incoming message
        self.process_message(message.body)

    def process_message(self, message_body):
        # Process the message - this method can be overridden or customized
        processed_data = message_body.decode('utf-8').upper()
        return processed_data
    