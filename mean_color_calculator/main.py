import json

import numpy as np

from mq_messaging import RMQProducer, RMQConsumer


class CalculatorInputValidator:
    pass


class AverageColorCalculator:
    COLOR_MAPPING = {0: 'red', 1: 'green', 2: 'blue'}

    def __init__(self, image):
        self.image = image

    def calculate_average_color(self):
        return self.COLOR_MAPPING[np.argmax(np.mean(np.mean(self.image, axis=0), axis=0))]


class CalculatorHandler:
    def __init__(self, host):
        self.mq_producer = RMQProducer('calculation_output', host)
        self.mq_consumer = RMQConsumer('calculation_request', host)
        self.mq_consumer.consume(self.callback_for_calculation)

    def callback_for_calculation(self, ch, method, properties, body):
        body_dict = json.loads(body)
        image_name = body_dict["image_name"]
        image_array = np.array(body_dict["image"])
        print(f'Calculating average color for image {image_name}')
        average_color = AverageColorCalculator(image_array).calculate_average_color()
        new_body = {"image_name": image_name,
                    "image": body_dict["image"],
                    "average_color": average_color}
        self.mq_producer.publish(json.dumps(new_body))


if __name__ == '__main__':
    CalculatorHandler('rabbitmq')
