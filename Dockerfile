#Deriving the latest base image
FROM python:3.9.13

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./ /usr/src/app/

RUN pip install -r requirements.txt


ENV bot_token=''
ENV webhook_url=''
ENV group_id=''
ENV bot_destroy_message='Бот обнаружен и уничтожен!'
ENV bot_status_check_message='👺😎Антиботская защита комьюнити включена!'
ENV seconds_after_member_join='30'
ENV status_check_command='!бот_статус'

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD ["python", "main.py"]