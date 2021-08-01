import glob
import json
import os
import time

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
        self.mq_producer = RMQProducer('calculation_request', host)

    def select_images_in_folder(self):

        return [x for x in glob.glob(self.path_to_image_dir + "/*")]

    def send_images(self):

        sent_images = set()

        while True:

            list_of_images = set(self.select_images_in_folder())
            diff = list_of_images - sent_images

            if diff:
                for image_path in diff:

                    image = ImageReader.read_image(image_path)

                    body = {"image_name": os.path.basename(image_path),
                            "image": image.tolist()}

                    self.mq_producer.publish(json.dumps(body))
                    sent_images = sent_images.union(diff)
            else:
                pass

            time.sleep(5)


if __name__ == '__main__':
    ReaderHandler('rabbitmq').send_images()
