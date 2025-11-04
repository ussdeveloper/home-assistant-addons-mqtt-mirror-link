ARG BUILD_FROM
FROM $BUILD_FROM

# Set working directory
WORKDIR /app

# Install required Python packages
RUN pip3 install --no-cache-dir paho-mqtt==1.6.1

# Copy application files
COPY mqtt_bridge.py /app/
COPY run.sh /
RUN chmod a+x /run.sh

# Run
CMD [ "/run.sh" ]
