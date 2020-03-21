FROM python:3

RUN mkdir -p /usr/src/izi

WORKDIR /usr/src/izi

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

RUN pip install --editable .

ENTRYPOINT [ "izi" ]

CMD [ "--help" ]