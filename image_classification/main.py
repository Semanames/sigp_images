import json

import cv2
import numpy as np

from mq_messaging import RMQConsumer


class ImageClassifier:

    def __init__(self, calculation_output_data, output_classification_path='./processed_images'):
        self.output_classification_path = output_classification_path
        self.calculation_output_data = calculation_output_data

    def classify(self):
        image_name = self.calculation_output_data["image_name"]
        image = np.array(self.calculation_output_data["image"])
        average_color = self.calculation_output_data["average_color"]

        print(f'Classifying image {image_name}')

        new_image_path = self.output_classification_path + "/" + average_color + "/" + image_name
        cv2.imwrite(new_image_path, image)


class ClassificationHandler:
    def __init__(self, host):
        self.mq_consumer = RMQConsumer('calculation_output', host)
        self.mq_consumer.consume(ClassificationHandler.classification_callback)

    @staticmethod
    def classification_callback(ch, method, properties, body):
        calculation_output_data = json.loads(body)
        ImageClassifier(calculation_output_data).classify()


if __name__ == '__main__':
    ClassificationHandler('localhost')
