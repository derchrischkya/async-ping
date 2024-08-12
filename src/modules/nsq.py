import gnsq
import elasticapm


class NSQPublisher:
    def __init__(self):
        self.producer = gnsq.Producer("127.0.0.1:14150")
        self.producer.start()

    def publish(self, topic: str, message: str) -> None:
        with elasticapm.capture_span(
            name="publish_message", span_subtype="nsq", span_action="publish", span_type="message_broker"
        ):
            self.producer.publish(topic, message)
