FROM python:3.9.7-alpine

LABEL image for a very simple flask application

WORKDIR /docker-flask

COPY . /docker-flask

RUN pip install requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]

