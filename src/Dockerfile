FROM python:3.8.12-alpine3.14

WORKDIR /backend

# for dev and debugging
#RUN pip3 install awscli --upgrade --user

COPY . /backend/src

RUN pip3 install -r /backend/src/requirements.txt

CMD [ "python3", "-m" , "src.app"]
