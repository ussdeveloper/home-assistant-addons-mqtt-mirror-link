ARG BUILD_FROM
FROM $BUILD_FROM

# Set working directory
WORKDIR /app

# Install Node.js 20 and npm
RUN apk add --no-cache \
    nodejs \
    npm

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies (production only)
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/

# Build TypeScript
RUN npm run build

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

# Run
CMD [ "/run.sh" ]
