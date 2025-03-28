FROM node:14-alpine

WORKDIR /app

# Copiar y construir el backend
COPY server/package*.json ./server/
RUN cd server && npm install
COPY server/ ./server/

# Copiar y construir el frontend
COPY client/package*.json ./client/
RUN cd client && npm install
COPY client/ ./client/
RUN cd client && npm run build

# Exponer puerto
EXPOSE 3000

# Iniciar el servidor
CMD ["node", "server/server.js"]