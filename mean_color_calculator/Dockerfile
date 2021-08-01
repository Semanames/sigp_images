FROM python:3.7

COPY . ./work
WORKDIR ./work

RUN pip3 install -r ./requirements.txt

ENTRYPOINT ["python", "main.py"]
