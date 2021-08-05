# SIGP Images

### General
This repository is dedicated to simple micro-service system for image classification based on its average color  <br />
System of microservices is communication through RabbitMQ message broker. <br />
There are three subservices :  <br />
* **Image Pusher** -`/sigp_images/image_pusher` - looking for files in directory `image_pusher/images_to_process/`
  validating them and sending them to RabbitMQ queue with name `calculation_request`
* **Mean Color Calculator** -`/sigp_images/mean-color_calculator`- processing the image from the queue `calculation_request` 
  and calculating average color of picture based on most abundant color. 
  This information is processed and sent to the RabbitMQ queue named `calculation_output`
* **Image Classifier** -`/sigp_images/mean-color_calculator`- consuming the message from the queue `calculation_output` 
  and processing it based on the information of average color and sending the image to the directory 
  `/image_classification/processed_images/<average_color>` 

Each of these microservices (RabbitMQ, Image Pusher, Mean Color Calculator, Image Classifier) are running 
as `Docker` container orchestrated by `docker-compose`. These tools you can download here:<br />
> https://www.docker.com/get-started <br />
> https://docs.docker.com/compose/install/

### Basic commands
To initiate our microservice architecture you should run this command from the root of this project:<br />
`docker-compose up` <br />
To terminate this session: 
`docker-compose down` <br />
To rebuild the Docker images:
`docker-compose build`

### Information about the subservices
Each subservice folder is holding several modules:
* main.py - holding core functionality - also could be run locally by `python main.py` ( with running RabbitMQ )
* test_main.py - testing core functionality
* mq_messaging.py - communication with RabbitMQ
* logger.py - logging
* requirements.txt - requirements for each microservice (needed during build)
* Dockerfile - for building Docker image

Microservices as Image Pusher and Image Classifier have mounted volumes <br /> 
`/image_classification/processed_images/`, `image_pusher/images_to_process/`<br />
inside Docker container so they are accessible 
from outside of the Docker container (However this works correctly on Linux and on Windows it has strange behaviour) 
