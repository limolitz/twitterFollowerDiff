FROM python:3.9-alpine

RUN addgroup tfd && adduser \
    --disabled-password \
    --gecos "" \
    --home /home/tfd \
    --ingroup tfd \
    --uid "1241" \
    tfd

USER tfd

WORKDIR /home/tfd

RUN python3 -m venv .

COPY --chown=tfd:tfd requirements.txt ./

RUN ./bin/pip install --no-cache-dir --disable-pip-version-check wheel && \
    ./bin/pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

COPY --chown=tfd:tfd main.py ./

ENTRYPOINT ["/home/tfd/bin/python3", "/home/tfd/main.py"]
