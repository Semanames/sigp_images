import json

import numpy as np

from mean_color_calculator.logger import logger
from mq_messaging import RMQProducer, RMQConsumer


class ColorCalculationConfig:

    IMAGE_REQUEST_QUEUE = 'calculation_request'
    IMAGE_PROCESSED_QUEUE = 'calculation_output'
    IMAGE_NAME = "image_name"
    IMAGE_ARRAY = "image"
    AVERAGE_COLOR = "average_color"
    MQ_BROKER = 'rabbitmq'
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class CalculatorInputValidator:
    pass


class AverageColorCalculator:
    COLOR_MAPPING = {0: ColorCalculationConfig.BLUE,
                     1: ColorCalculationConfig.GREEN,
                     2: ColorCalculationConfig.RED}

    def __init__(self, image):
        self.image = image

    def calculate_average_color(self):
        return self.COLOR_MAPPING[np.argmax(np.mean(np.mean(self.image, axis=0), axis=0))]


class CalculatorHandler:
    def __init__(self, host):
        self.mq_producer = RMQProducer(ColorCalculationConfig.IMAGE_PROCESSED_QUEUE, host)
        self.mq_consumer = RMQConsumer(ColorCalculationConfig.IMAGE_REQUEST_QUEUE, host)
        logger.info('Mean Color Calculator connected to the RMQ')
        self.mq_consumer.consume(self.callback_for_calculation)
        logger.info('Mean Color Calculator: Consuming images from RMQ')

    def callback_for_calculation(self, ch, method, properties, body):
        body_dict = json.loads(body)

        image_name = body_dict[ColorCalculationConfig.IMAGE_NAME]
        image_array = np.array(body_dict[ColorCalculationConfig.IMAGE_ARRAY])

        logger.info(f'Calculating average color for image {image_name}')
        average_color = AverageColorCalculator(image_array).calculate_average_color()

        new_body = {ColorCalculationConfig.IMAGE_NAME: image_name,
                    ColorCalculationConfig.IMAGE_ARRAY: body_dict[ColorCalculationConfig.IMAGE_ARRAY],
                    ColorCalculationConfig.AVERAGE_COLOR: average_color}

        self.mq_producer.publish(json.dumps(new_body))


if __name__ == '__main__':
    CalculatorHandler(ColorCalculationConfig.MQ_BROKER)
