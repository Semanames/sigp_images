import glob
import json
import os
import time

import cv2

from logger import logger
from mq_messaging import RMQProducer


class ImageReaderConfig:
    IMAGE_REQUEST_QUEUE = 'calculation_request'
    IMAGE_NAME = "image_name"
    IMAGE_ARRAY = "image"
    IMAGES_TO_PROCESS_PATH = './images_to_process'
    MQ_BROKER = 'rabbitmq'
    TIME_CHECK_PERIOD = 5


class ImageReaderInputValidator:
    pass


class ImageReader:

    @staticmethod
    def read_image(path_to_image):
        img = cv2.imread(path_to_image)
        return img


class ReaderHandler:

    def __init__(self, host, path_to_image_dir=ImageReaderConfig.IMAGES_TO_PROCESS_PATH):
        self.path_to_image_dir = path_to_image_dir
        self.mq_producer = RMQProducer(ImageReaderConfig.IMAGE_REQUEST_QUEUE, host)
        logger.info('Image Reader connected to the RMQ')

    def select_images_in_folder(self):

        return [x for x in glob.glob(self.path_to_image_dir + "/*")]

    def send_images(self, delta_t=ImageReaderConfig.TIME_CHECK_PERIOD):

        sent_images = set()
        logger.info(f'Image Reader: Pushing for images from {ImageReaderConfig.IMAGES_TO_PROCESS_PATH}  to RMQ')

        while True:

            list_of_images = set(self.select_images_in_folder())
            diff = list_of_images - sent_images

            if diff:
                for image_path in diff:
                    image = ImageReader.read_image(image_path)
                    if image is not None:

                        body = {ImageReaderConfig.IMAGE_NAME: os.path.basename(image_path),
                                ImageReaderConfig.IMAGE_ARRAY: image.tolist()}

                        self.mq_producer.publish(json.dumps(body))
                        sent_images = sent_images.union(diff)
                    else:
                        pass
            else:
                pass

            time.sleep(delta_t)


if __name__ == '__main__':
    ReaderHandler(ImageReaderConfig.MQ_BROKER).send_images()
