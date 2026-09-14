# Secure Microservice Task Queue API — Dockerization Practice

## My Focus: Learning Docker Through Containerization

My primary contribution to this project was containerizing an existing Python application to practice Docker and understand how applications are packaged and run inside containers.

The application code was provided to me for practice. I did not write or develop the Python task queue application logic. Instead, I studied the application's requirements and created the Dockerfile myself to practice:

* Multi-stage Docker builds
* Dependency installation
* Docker image structure
* File paths between build stages
* Working directories
* Non-root container execution
* File permissions
* Port configuration
* Container startup commands

This project is focused on my Docker learning rather than application development.

---

## Project Overview

The **Secure Microservice Task Queue API** is a small Python Flask application that uses SQLite for task storage and Gunicorn as the application server.

For this exercise, my focus was on creating a Docker image that packages the application and its dependencies into a runnable container.

The application runs as a **single container**, so no Docker network or second container is required for this exercise.

### Technologies

* Python
* Flask
* Gunicorn
* SQLite
* Docker
* Alpine Linux

---

# Docker Implementation

I used a **multi-stage Dockerfile** with two stages:

```text
Stage 1: Builder
    |
    | Install Python dependencies
    v
/install
    |
    | COPY --from=builder
    v
Stage 2: Runtime
    |
    | Application + dependencies
    | Non-root user
    v
Final Docker Image
```

The purpose of separating the build and runtime stages is to keep the final image focused on what is required to run the application.

---

# Dockerfile

```dockerfile
# --- Stage 1: Build Stage ---
FROM python:3.11-alpine AS builder

# Creating the directory it will start working on
WORKDIR /app

# Copying my dependency file into the current directory /app
COPY requirements.txt .

# Install dependencies into /install and --no-cache-dir tells pip not to keep the downloaded packages
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Runtime Stage ---
FROM python:3.11-alpine AS runtime

WORKDIR /app

# Copying dependency from builder
COPY --from=builder /install /usr/local

# Copying the main file into the current directory
COPY app.py .

# Creating the user named bmuser and giving it permissions to the file
RUN adduser -D bmuser && chown -R bmuser:bmuser /app

# Run the app as non root user
USER bmuser

# Flask listens on port 5000
EXPOSE 5000

# Starting the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

# Stage 1: Build Stage

```dockerfile
FROM python:3.11-alpine AS builder
```

This creates the first stage using Python 3.11 on Alpine Linux.

I named the stage:

```text
builder
```

so that I can refer to it later.

### Working Directory

```dockerfile
WORKDIR /app
```

This creates `/app` as the working directory inside the builder stage.

### Copy Dependencies

```dockerfile
COPY requirements.txt .
```

This copies `requirements.txt` from my project directory into `/app` inside the container.

### Install Dependencies

```dockerfile
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

The dependencies are installed into:

```text
/install
```

The `--no-cache-dir` option prevents pip from keeping its downloaded package cache.

The important Docker concept I practiced here is that the dependencies are deliberately installed into a separate location so they can be copied into the runtime stage.

---

# Stage 2: Runtime Stage

```dockerfile
FROM python:3.11-alpine AS runtime
```

This starts a new image stage for running the application.

The runtime stage is separate from the builder stage.

### Working Directory

```dockerfile
WORKDIR /app
```

The application will work from `/app`.

### Copy Dependencies From Builder

```dockerfile
COPY --from=builder /install /usr/local
```

This was one of the main Docker concepts I practiced.

It means:

```text
From the builder stage:
    /install

Copy it into the runtime stage:
    /usr/local
```

The dependencies installed during Stage 1 are therefore available in Stage 2.

### Copy Application Code

```dockerfile
COPY app.py .
```

This copies `app.py` from my project directory into the current working directory:

```text
/app/app.py
```

---

# Running as a Non-Root User

```dockerfile
RUN adduser -D bmuser && chown -R bmuser:bmuser /app
USER bmuser
```

I created a non-root user called `bmuser` and gave that user ownership of the application directory.

The container then runs the application as:

```text
bmuser
```

instead of the default root user.

This allowed me to practice the Docker concept of running containers with a non-root user.

---

# Port Configuration

```dockerfile
EXPOSE 5000
```

The Flask/Gunicorn application listens on port `5000` inside the container.

When running the container, I map my host port `1912` to the container's port `5000`:

```text
Host                  Container
1912       ------>    5000
```

This is done with:

```bash
-p 1912:5000
```

---

# Starting the Container

The application is started with:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

This tells Docker to start Gunicorn and bind the application to port `5000`.

---

# Project Structure

```text
secure-task-queue-api/
│
├── app.py
├── requirements.txt
└── Dockerfile
```

### `app.py`

The provided Flask application.

### `requirements.txt`

Contains the Python dependencies:

```text
flask==3.0.0
gunicorn==21.2.0
```

### `Dockerfile`

The Docker configuration I created to containerize the application.

---

# Building the Docker Image

I built the Docker image with:

```bash
docker build -t task-queue-api-image .
```

Breakdown:

```text
docker build       Build an image
-t task-queue-api  Give the image a name
.                  Use the current directory as the build context
```

The resulting image is named:

```text
task-queue-api
```

---

# Running the Container

I run the image as a detached container with:

```bash
docker run -d --name my_task_api -p 1409:5000 task-queue-api-image
```

Breakdown:

```text
docker run              Create and start a container
-d                      Run in detached mode
--name my_task_api     Give the container a name
-p 1409:5000           Map host port 1409 to container port 5000
task-queue-api         Use the Docker image
```

For this exercise, I am focusing on successfully building the Docker image and starting the container. I am not testing or developing the API functionality.

---

# Docker Concepts Practiced

Through this project, I practiced:

1. Multi-stage Docker builds
2. Builder and runtime stages
3. `FROM`
4. `AS`
5. `WORKDIR`
6. `COPY`
7. `COPY --from`
8. Installing dependencies inside an image
9. Understanding source and destination paths
10. Running containers as a non-root user
11. File ownership with `chown`
12. `EXPOSE`
13. `CMD`
14. Docker image naming
15. Port mapping with `-p`
16. Running containers in detached mode with `-d`
17. Understanding the difference between an image and a container

---

# Key Learning Outcome

The main goal of this project was not to develop the Python application.

My goal was to understand how to take an existing application and create a Docker image that contains what is required to run it.

In particular, I practiced understanding:

* What belongs in the builder stage
* What belongs in the runtime stage
* How dependencies move from one stage to another
* How `COPY --from=builder` works
* How Docker paths work
* How a container starts an application
* How port mapping works
* Why running as a non-root user is useful
* The difference between building an image and running a container

---

# Scope & Transparency

The Python application code was provided to me as a practice application.

I did **not** write the Flask task queue application logic.

My contribution to this exercise was creating and understanding the Dockerfile and using Docker to build and run the application as a container.

This project therefore represents my **Docker/containerization practice**, rather than claiming ownership of the underlying application development.

---

# Next Steps

After becoming comfortable with these Docker fundamentals, my planned progression is:

* Docker networking
* Docker volumes
* Docker Compose
* Docker image optimization
* Docker build caching
* Container security
* Amazon ECR
* Amazon ECS/Fargate

---

# About This Project

This project is part of my hands-on learning journey toward **Cloud Engineering and Cloud Infrastructure**.

I am using small practical projects to build a stronger understanding of Docker, AWS, Terraform, infrastructure, and cloud deployment concepts.
