import glob
import json
import os

import cv2

from mq_messaging import RMQProducer


class ImageReader:
    @staticmethod
    def read_image(path_to_image):
        img = cv2.imread(path_to_image)
        return img


class ReaderHandler:

    def __init__(self, host, path_to_image_dir='./images_to_process'):
        self.path_to_image_dir = path_to_image_dir
        self.list_of_images = [os.path.basename(x) for x in glob.glob(self.path_to_image_dir + "/*")]
        self.paths_to_images = [self.path_to_image_dir + "/" + image_name for image_name in self.list_of_images]
        self.mq_producer = RMQProducer('calculation_request', host)

    def send_images(self):
        for image_name, image_path in zip(self.list_of_images, self.paths_to_images):
            image = ImageReader.read_image(image_path)
            body = {"image_name": image_name,
                    "image": image.tolist()}
            self.mq_producer.publish(json.dumps(body))


if __name__ == '__main__':
    ReaderHandler('localhost').send_images()
