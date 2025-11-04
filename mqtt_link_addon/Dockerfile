ARG BUILD_FROM
FROM $BUILD_FROM

# Zainstaluj wymagane pakiety
RUN apk add --no-cache \
    python3 \
    py3-pip \
    && pip3 install --no-cache-dir paho-mqtt==1.6.1

# Skopiuj pliki aplikacji
COPY mqtt_bridge.py /app/
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
