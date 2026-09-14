#Stage 1: build stage
FROM python:3.11-alpine AS builder

#Creating the directory it will start working on
WORKDIR /app

#copying my dependency file into the current directory /app
COPY requirements.txt  .

#Install dependencies into /install and -no-cache-dir tells pip not to keep the downloaded package cache 
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


#stage 2: runtime stage
FROM python:3.11-alpine AS runtime

WORKDIR /app

#copying dependency from builder
COPY --from=builder /install /usr/local

#copying the main file into the current directory
COPY app.py  .

#creating the user named bmuser and giving it permissions to the file
RUN adduser -D bmuser && chown -R bmuser:bmuser /app

#run the app as non root user
USER bmuser

#flask listens on port 5000
EXPOSE 5000

#starting the application
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]