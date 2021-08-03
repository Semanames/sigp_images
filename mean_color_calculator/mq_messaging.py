import pika


class BaseRMQMessaging:
    def __init__(self, queue, host):
        self.queue = queue
        self.host = host

        while True:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                break
            except Exception:
                pass

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def close_connection(self):
        self.connection.close()


class RMQProducer(BaseRMQMessaging):

    def publish(self, payload, exchange=''):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=self.queue,
                                   body=payload)


class RMQConsumer(BaseRMQMessaging):

    def consume(self, callback):
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()
