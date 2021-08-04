import json
import os

import cv2
import numpy as np
import webcolors

from logger import logger
from mq_messaging import RMQConsumer


class ImageClassifierConfig:
    IMAGE_PROCESSED_QUEUE = 'calculation_output'
    IMAGE_NAME = "image_name"
    IMAGE_ARRAY = "image"
    AVERAGE_COLOR = "average_color"
    MQ_BROKER = 'rabbitmq'
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    PROCESSED_IMAGES_PATH = './processed_images'


class ImageClassifierInputValidator:
    input_data_keys = {ImageClassifierConfig.IMAGE_NAME,
                       ImageClassifierConfig.IMAGE_ARRAY,
                       ImageClassifierConfig.AVERAGE_COLOR}

    average_color_fields = set(webcolors.CSS3_NAMES_TO_HEX.keys())

    @classmethod
    def validate_calculation_output_data(cls, calculation_output_data):
        if cls.input_data_keys.issubset(set(calculation_output_data.keys())):
            if not calculation_output_data[ImageClassifierConfig.AVERAGE_COLOR] in cls.average_color_fields:
                raise ValueError(f'{calculation_output_data[ImageClassifierConfig.AVERAGE_COLOR]}' +
                                 f' is not among {cls.average_color_fields}')

            return calculation_output_data
        else:
            missing_keys = cls.input_data_keys - set(calculation_output_data.keys())
            raise ValueError(f'There are missing keys {missing_keys} in input data: {calculation_output_data}')


class ImageClassifier:

    def __init__(self, calculation_output_data, output_classification_path=ImageClassifierConfig.PROCESSED_IMAGES_PATH):
        self.output_classification_path = output_classification_path
        self.calculation_output_data = ImageClassifierInputValidator.validate_calculation_output_data(
            calculation_output_data)

    def classify(self):
        image_name = self.calculation_output_data[ImageClassifierConfig.IMAGE_NAME]
        image = np.array(self.calculation_output_data[ImageClassifierConfig.IMAGE_ARRAY])
        average_color = self.calculation_output_data[ImageClassifierConfig.AVERAGE_COLOR]

        logger.info(f'Classifying image {image_name}')

        base_path = self.output_classification_path + "/" + average_color

        if not os.path.exists(base_path):
            os.mkdir(base_path)

        new_image_path = base_path + "/" + image_name
        cv2.imwrite(new_image_path, image)


class ClassificationHandler:
    def __init__(self, host):
        self.mq_consumer = RMQConsumer(ImageClassifierConfig.IMAGE_PROCESSED_QUEUE, host)
        self.mq_consumer.consume(ClassificationHandler.classification_callback)
        logger.info('Image Classifier connected to the RMQ')

    @staticmethod
    def classification_callback(ch, method, properties, body):
        calculation_output_data = json.loads(body)
        try:
            image_classifier = ImageClassifier(calculation_output_data)
        except ValueError as exc:
            logger.error(exc_info=str(exc))
            return
        image_classifier.classify()


if __name__ == '__main__':
    ClassificationHandler(ImageClassifierConfig.MQ_BROKER)
