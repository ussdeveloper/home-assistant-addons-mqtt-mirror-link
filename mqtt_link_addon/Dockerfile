ARG BUILD_FROM
FROM $BUILD_FROM

# Set working directory
WORKDIR /app

# Install Node.js 20 and npm (using nodejs-current for v20+)
RUN apk add --no-cache \
    nodejs-current \
    npm

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies including devDependencies for build
RUN npm ci

# Copy source code
COPY src/ ./src/

# Build TypeScript
RUN npm run build

# Remove devDependencies to reduce image size
RUN npm prune --production

# Copy startup script
COPY run.sh /
RUN chmod a+x /run.sh

# Run
CMD [ "/run.sh" ]
