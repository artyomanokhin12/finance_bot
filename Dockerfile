FROM python:3.12

RUN mkdir /bot

WORKDIR /bot

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /bot/docker_run.sh