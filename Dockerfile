#Deriving the latest base image
FROM python:3.9.13

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./ /usr/src/app/

RUN pip install -r requirements.txt

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD ["python", "main.py"]