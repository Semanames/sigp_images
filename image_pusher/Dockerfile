FROM python:3.7

COPY . ./work
WORKDIR ./work

RUN apt-get update && apt-get install -y python3-opencv
RUN pip3 install -r ./requirements.txt

ENTRYPOINT ["python", "main.py"]
