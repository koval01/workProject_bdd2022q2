FROM python:3.9.13

ENV APP_ROOT /app
ENV CONFIG_ROOT /config


RUN mkdir ${CONFIG_ROOT}
COPY requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip install -r ${CONFIG_ROOT}/requirements.txt

RUN python3 imgcollector/manage.py collectstatic

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

ADD . ${APP_ROOT}