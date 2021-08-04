FROM python:3.7

COPY requirements.txt /work/requirements.txt
WORKDIR /work


RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install -r ./requirements.txt

COPY . .

CMD ["pytest", "test_main.py"]

CMD ["python", "main.py"]
