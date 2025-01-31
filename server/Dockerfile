FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /server

# Copy the server directory contents
COPY server/ .

RUN apt-get update && apt-get install -y 
# Copy requirements.txt from the root
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

