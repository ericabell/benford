FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN mkdir /app/tmp
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
