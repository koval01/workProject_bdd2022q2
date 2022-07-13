FROM python:3.9.13

ENV APP_ROOT /app
ENV CONFIG_ROOT /config


RUN mkdir ${CONFIG_ROOT}
COPY requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip install -r ${CONFIG_ROOT}/requirements.txt

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

ADD . ${APP_ROOT}

#RUN python ${APP_ROOT}/manage.py makemigrations
#RUN python ${APP_ROOT}/manage.py migrate

RUN mkdir -p /app/static
#RUN python ${APP_ROOT}/manage.py collectstatic --no-input