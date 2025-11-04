ARG BUILD_FROM
FROM $BUILD_FROM

# Ustaw katalog roboczy
WORKDIR /app

# Zainstaluj wymagane pakiety Python
RUN pip3 install --no-cache-dir paho-mqtt==1.6.1

# Skopiuj pliki aplikacji
COPY mqtt_bridge.py /app/
COPY run.sh /
RUN chmod a+x /run.sh

# Uruchom
CMD [ "/run.sh" ]
