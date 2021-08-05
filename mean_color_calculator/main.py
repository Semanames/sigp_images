import json
from typing import List, Union

import numpy as np
import webcolors

from logger import logger
from mq_messaging import RMQProducer, RMQConsumer


class ColorCalculationConfig:
    '''
    Config for calculation
    '''

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
    '''
    Class for validating input to AverageColorCalculator
    '''

    @staticmethod
    def validate_image_input(image_input):

        '''
        Validates image input comming from Rabbit MQ
        :param image_input:
        :return: image_input or raise error
        '''

        if type(image_input) == list:
            if type(image_input[0]) == list:
                if type(image_input[0][0]) == list and len(image_input[0][0]) == 3:
                    if type(image_input[0][0][0]) == int:
                        return image_input
                    else:
                        raise TypeError(f'Image is not in correct format, it should be in BGR format')
                else:
                    raise TypeError(f'Image is not in correct format, it should be in BGR format')
            else:
                raise TypeError(f'Image is not in correct format, it should be in BGR format')
        else:
            raise TypeError(f'Image is not in correct format, it should be in BGR format')


class AverageColorCalculator:
    '''
    Class for calculation mean color value of an image
    '''

    def __init__(self, image: np.ndarray):
        self.image = image

    def calculate_average_color(self):

        '''
        Calculates average color value of self.image
        :return: str: name of the most abundant color of an image from WebColors
        '''

        color_count = {}
        dim = self.image.shape
        for i in range(dim[0]):
            for j in range(dim[1]):
                color = self.nearest_color(self.image[i, j])
                if color in color_count.keys():
                    color_count[color] += 1
                else:
                    color_count[color] = 1
        return sorted(color_count.keys(), key=lambda color_name: color_count[color_name])[-1]

    @staticmethod
    def nearest_color(requested_colour: Union[List, np.ndarray]):
        '''
        Calculates nearest color from Webcolors palette from BGR coordinate in RGB space
        :param requested_colour: np.ndarray or list, list of three coordinates
        :return: str, color of one pixel with given BGR coordinates
        '''
        min_colors = {}
        for key, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[2]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[0]) ** 2
            min_colors[(rd + gd + bd)] = color_name
        return min_colors[min(min_colors.keys())]


class CalculatorHandler:
    '''
    Class for handling messages from RabbitMQ a processing them for calculation
    '''

    def __init__(self, host: str):
        self.mq_producer = RMQProducer(ColorCalculationConfig.IMAGE_PROCESSED_QUEUE, host)
        self.mq_consumer = RMQConsumer(ColorCalculationConfig.IMAGE_REQUEST_QUEUE, host)
        logger.info('Mean Color Calculator connected to the RMQ')
        self.mq_consumer.consume(self.callback_for_calculation)
        logger.info('Mean Color Calculator: Consuming images from RMQ')

    def callback_for_calculation(self, ch, method, properties, body):
        body_dict = json.loads(body)

        image_name = body_dict[ColorCalculationConfig.IMAGE_NAME]
        try:
            image = CalculatorInputValidator.validate_image_input(body_dict[ColorCalculationConfig.IMAGE_ARRAY])
        except TypeError as exc:
            logger.error(str(exc))
            return
        image_array = np.array(image)

        logger.info(f'Calculating average color for image {image_name}')
        average_color = AverageColorCalculator(image_array).calculate_average_color()

        new_body = {ColorCalculationConfig.IMAGE_NAME: image_name,
                    ColorCalculationConfig.IMAGE_ARRAY: body_dict[ColorCalculationConfig.IMAGE_ARRAY],
                    ColorCalculationConfig.AVERAGE_COLOR: average_color}

        self.mq_producer.publish(json.dumps(new_body))


if __name__ == '__main__':
    CalculatorHandler(ColorCalculationConfig.MQ_BROKER)
