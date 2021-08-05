from typing import Callable

import pika


class BaseRMQMessaging:
    '''
    Base class for RMQ Producers and consumers
    '''
    def __init__(self, queue: str, host: str):
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
        '''
        Closing connection
        :return:
        '''
        self.connection.close()


class RMQProducer(BaseRMQMessaging):
    '''
    RMQ producer class
    '''
    def publish(self, payload, exchange: str = ''):
        '''
        Publishes messages to RMG queue
        :param payload:
        :param exchange: RMQ exchange name for directing messages to the queues
        :return:
        '''
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=self.queue,
                                   body=payload)


class RMQConsumer(BaseRMQMessaging):
    '''
    RMQ consumer class
    '''
    def consume(self, callback: Callable):
        '''
        Consumes messages from given queue
        :param callback: callback method to be called when message is consumed
        :return:
        '''
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()
