FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . mining
RUN pip3 install -r mining/requirements.txt
ENTRYPOINT ["python3"]
CMD ["mining/main.py"]

