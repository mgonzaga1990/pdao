FROM python:3.8.3


RUN apt-get update \
    && apt-get install -y --no-install-recommends pdftk \
    && rm -Rf /var/lib/apt/lists/*

ENV APP_ROOT /app
ENV CONFIG_ROOT /config

RUN mkdir ${CONFIG_ROOT}
COPY requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip install -r ${CONFIG_ROOT}/requirements.txt

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

EXPOSE 8000

ADD . ${APP_ROOT}

#collect static
RUN python manage.py collectstatic --noinput
