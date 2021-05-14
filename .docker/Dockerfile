FROM python:3.9-slim-buster

ENV VAULT_ADDR 127.0.0.1
ENV VAULT_TOKEN foo

COPY bin /app/bin
COPY vmb /app/vmb
COPY backup.sh /app/backup.sh
COPY setup.py /app/setup.py
COPY README.md /app/README.md

RUN ln -s /app/backup.sh /usr/bin/vault-kv-backup

RUN cd /app  \
        && python3 setup.py install

WORKDIR /app
ENTRYPOINT ["python3"]
