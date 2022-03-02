FROM python:3.7-alpine3.14

WORKDIR /backend

RUN pip3 install awscli --upgrade --user

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /backend/src

ENV FLASK_APP=/backend/src/app.py

EXPOSE 5000

CMD [ "python3", "-m" , "src.app"]
