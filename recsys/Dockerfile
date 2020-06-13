FROM python:3.8.2

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ = ${TZ}

RUN mkdir online_store && mkdir online_store/recsys

WORKDIR /online_store/recsys

ADD ./ /online_store/recsys
ADD ./requirements.txt /online_store/recsys/requirements.txt

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install --upgrade pip
RUN pip install torch==1.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install -r /online_store/recsys/requirements.txt