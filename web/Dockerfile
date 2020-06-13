FROM python:3.8.2

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ = ${TZ}

RUN mkdir online_store && mkdir online_store/web

WORKDIR /online_store/web

ADD ./ /online_store/web
ADD ./requirements.txt /online_store/web/requirements.txt

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip
RUN pip install -r /online_store/web/requirements.txt