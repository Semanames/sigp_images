import json

import cv2
import numpy as np

from image_classification.logger import logger
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


class ImageClassifier:

    def __init__(self, calculation_output_data, output_classification_path=ImageClassifierConfig.PROCESSED_IMAGES_PATH):
        self.output_classification_path = output_classification_path
        self.calculation_output_data = calculation_output_data

    def classify(self):
        image_name = self.calculation_output_data[ImageClassifierConfig.IMAGE_NAME]
        image = np.array(self.calculation_output_data[ImageClassifierConfig.IMAGE_ARRAY])
        average_color = self.calculation_output_data[ImageClassifierConfig.AVERAGE_COLOR]

        logger.info(f'Classifying image {image_name}')

        new_image_path = self.output_classification_path + "/" + average_color + "/" + image_name
        cv2.imwrite(new_image_path, image)


class ClassificationHandler:
    def __init__(self, host):
        self.mq_consumer = RMQConsumer(ImageClassifierConfig.IMAGE_PROCESSED_QUEUE, host)
        self.mq_consumer.consume(ClassificationHandler.classification_callback)
        logger.info('Image Classifier connected to the RMQ')

    @staticmethod
    def classification_callback(ch, method, properties, body):
        calculation_output_data = json.loads(body)
        ImageClassifier(calculation_output_data).classify()


if __name__ == '__main__':
    ClassificationHandler(ImageClassifierConfig.MQ_BROKER)
