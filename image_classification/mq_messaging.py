import pika


class BaseRMQMessaging:
    def __init__(self, queue, host):
        self.queue = queue
        self.host = host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
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


if __name__ == '__main__':
    producer = RMQProducer(queue='hello', host='localhost')
    producer.publish('blablabla')
    consumer = RMQConsumer(queue='hello', host='localhost')

    def my_callback(ch, method, properties, body):
        print(body)
        return body

    consumer.consume(callback=my_callback)