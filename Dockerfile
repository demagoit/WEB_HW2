FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip

COPY web_hw2 /web_hw2
COPY requirements.txt /web_hw2/requirements.txt
WORKDIR /web_hw2

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]