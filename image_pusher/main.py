import glob
import json
import os
import time

import cv2

from logger import logger
from mq_messaging import RMQProducer
from pathlib import Path


class ImageReaderConfig:
    '''
    Config for pushing images
    '''
    IMAGE_REQUEST_QUEUE = 'calculation_request'
    IMAGE_NAME = "image_name"
    IMAGE_ARRAY = "image"
    IMAGES_TO_PROCESS_PATH = './images_to_process'
    MQ_BROKER = 'rabbitmq'
    TIME_CHECK_PERIOD = 5


class ImageReaderInputValidator:
    '''
    Class for validating input to ImageReader
    '''
    supported_extensions = ['.bmp', '.dib', '.jpg', '.jpe', '.jp2', '.png', '.webp',
                            '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.sr', '.ras',
                            '.tiff', '.tif', '.exr', '.hdr', '.pic']

    @classmethod
    def validate_input_file(cls, image_path: str):
        '''
        Validates filepath in ./images_to_process
        :param image_path:
        :return: bool or raise error
        '''
        if not Path(image_path).suffix in cls.supported_extensions:
            logger.error(f'File format for {os.path.basename(image_path)}' +
                         f' is not among {cls.supported_extensions}')
            return False
        return True


class ImageReader:
    '''
    Class for reading images
    '''

    @staticmethod
    def read_image(path_to_image: str):
        '''
        Reads image from image_path
        :return: np.ndarray: BGR array representation of an image
        '''
        if ImageReaderInputValidator.validate_input_file(path_to_image):
            img = cv2.imread(path_to_image)
            return img
        return None


class ImageReaderHandler:
    '''
    Class for pushing messages to RabbitMQ
    '''
    def __init__(self,
                 host: str,
                 path_to_image_dir: str = ImageReaderConfig.IMAGES_TO_PROCESS_PATH):

        self.path_to_image_dir = path_to_image_dir
        self.mq_producer = RMQProducer(ImageReaderConfig.IMAGE_REQUEST_QUEUE, host)
        logger.info('Image Reader connected to the RMQ')

    def select_images_in_folder(self):
        '''
        Creating list of file paths in given directory
        :return: list
        '''

        return [x for x in glob.glob(self.path_to_image_dir + "/*")]

    def send_images(self, delta_t: float = ImageReaderConfig.TIME_CHECK_PERIOD):
        '''
        Periodic check for new documents in directory, new documents are converted to BGR representation
        and sent to the RMQ queue
        :param delta_t: float, time check period
        :return:
        '''

        processed_images = set()
        logger.info(f'Image Reader: Pushing for images from {ImageReaderConfig.IMAGES_TO_PROCESS_PATH}  to RMQ')

        while True:

            list_of_images = set(self.select_images_in_folder())
            diff = list_of_images - processed_images

            if diff:
                for image_path in diff:
                    image = ImageReader.read_image(image_path)
                    if image is not None:

                        body = {ImageReaderConfig.IMAGE_NAME: os.path.basename(image_path),
                                ImageReaderConfig.IMAGE_ARRAY: image.tolist()}

                        self.mq_producer.publish(json.dumps(body))

                processed_images = processed_images.union(diff)

            time.sleep(delta_t)


if __name__ == '__main__':
    ImageReaderHandler(ImageReaderConfig.MQ_BROKER).send_images()
