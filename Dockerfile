FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app/frontend
COPY frontend/package*.json .
RUN npm install

COPY backend /app/backend
COPY frontend /app/frontend

EXPOSE 5000 3000

CMD sh -c "cd /app/backend && python app.py & cd /app/frontend && npm start"