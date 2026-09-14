# Distributed Rate-Limiter API Gateway — Dockerization Practice

##  My Focus: Learning Docker Through Containerization

**My primary contribution to this project was Dockerizing an existing Python application to strengthen my practical understanding of Docker and containerization.**

The application code was **provided to me for practice**. I did **not write or develop the Python rate-limiting application logic**. Instead, I studied the application's requirements and created the `Dockerfile` myself to practice applying Docker concepts I have been learning.

My focus was understanding how to take an existing application and turn it into a reproducible, isolated container while applying Docker best practices such as:

* Multi-stage Docker builds
* Build and runtime stage separation
* Dependency installation and transfer
* Docker image layering
* Working directories
* `COPY` behavior and source/destination paths
* Non-root container execution
* File ownership and permissions
* Container ports
* Gunicorn as the application server
* Understanding what belongs in the image versus what belongs in the application

This project is primarily a **Docker learning and containerization exercise**, rather than an application-development project.

---

## Project Overview

This project uses a Python Flask application that acts as an API Gateway-style proxy.

The provided application uses:

* **Flask** for the web application
* **Redis** for rate-limit data
* **Gunicorn** as the WSGI server
* **Requests** for forwarding requests to the backend

The application's logic implements a sliding-window rate limiter using Redis before forwarding requests to a backend service.

Again, the application itself was provided for this exercise. My work focused on understanding and containerizing it with Docker.

---

## Docker Implementation

I created a **multi-stage Dockerfile** consisting of two stages:

```text
Stage 1: Builder
        │
        ├── Python 3.11 Alpine
        ├── Copy requirements.txt
        └── Install dependencies into /install
                    │
                    ▼
Stage 2: Runtime
        │
        ├── Python 3.11 Alpine
        ├── Copy dependencies from builder
        ├── Copy application
        ├── Create non-root user
        ├── Change ownership
        └── Run application as non-root
```

### Stage 1 — Builder

The first stage is responsible for installing the Python dependencies.

```dockerfile
FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

### What I Practiced

The important concept I was learning here was:

```dockerfile
--prefix=/install
```

Instead of installing the dependencies directly into the normal Python environment, I installed them into:

```text
/install
```

This allowed me to transfer the installed dependencies into the final runtime stage using:

```dockerfile
COPY --from=builder /install /usr/local
```

This helped me understand one of the key concepts behind multi-stage Docker builds: **artifacts can be created in one stage and selectively copied into another stage.**

---

## Stage 2 — Runtime

The second stage contains what is required to run the application.

```dockerfile
FROM python:3.11-alpine AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app.py .

RUN adduser -D bmuser && chown -R bmuser:bmuser /app

USER bmuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Why I Structured It This Way

I wanted to understand the difference between:

**Build environment**

and

**Runtime environment**

The builder stage handles dependency installation, while the runtime stage receives the installed dependencies and application source needed to run the application.

This gave me practical experience with:

```text
COPY --from=builder
```

and understanding exactly where files are located in each Docker stage.

---

## Running as a Non-Root User

Another Docker concept I practiced was running the application as a non-root user.

Instead of leaving the container running as Docker's default `root` user, I created:

```dockerfile
RUN adduser -D bmuser
```

Then changed ownership of the application directory:

```dockerfile
RUN adduser -D bmuser && chown -R bmuser:bmuser /app
```

And switched the container to that user:

```dockerfile
USER bmuser
```

This helped me understand the importance of **least privilege inside containers** and how file ownership affects whether an application can access the files it needs.

---

##  Project Structure

```text
distributed-rate-limiter/
│
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

### File Responsibilities

| File               | Purpose                         |
| ------------------ | ------------------------------- |
| `app.py`           | Provided Python application     |
| `requirements.txt` | Python dependencies             |
| `Dockerfile`       | My Docker containerization work |
| `README.md`        | Project documentation           |

---

## 🛠️ Technologies

* **Docker**
* **Docker Multi-Stage Builds**
* **Python 3.11**
* **Alpine Linux**
* **Flask**
* **Gunicorn**
* **Redis**

---

## Building the Image

Build the Docker image with:

```bash
docker build -t rate-limiter-gateway-image .
```

Run the container:

```bash
docker run -d --name rate-limiter-gateway-image-container -p 1912:5000 rate-limiter-gateway-image
```

The application will then be available on:

```text
http://localhost:1912
```

---

## Docker Concepts Practiced

This project was specifically useful for reinforcing the following Docker concepts:

### 1. Multi-Stage Builds

Understanding why a Dockerfile can have multiple `FROM` instructions and how files can be transferred between stages.

### 2. `WORKDIR`

Understanding how:

```dockerfile
WORKDIR /app
```

sets the working directory for subsequent Dockerfile instructions.

### 3. `COPY`

Practicing the difference between copying files from the local build context:

```dockerfile
COPY app.py .
```

and copying files from another Docker build stage:

```dockerfile
COPY --from=builder /install /usr/local
```

### 4. Dependency Installation

Understanding how Python dependencies are installed during the image build process and made available to the runtime container.

### 5. Non-Root Containers

Practicing how to create a dedicated user and run the application without root privileges.

### 6. File Permissions

Understanding why the application directory needs appropriate ownership when switching from `root` to an unprivileged user.

### 7. Container Ports

Understanding the role of:

```dockerfile
EXPOSE 5000
```

and how it relates to Docker's runtime port mapping.

### 8. Container Startup

Understanding how the `CMD` instruction determines the default process executed when the container starts.

---

## Key Learning Outcome

The biggest takeaway from this project was learning to think about Docker as a **containerization layer around an application**.

Rather than focusing on writing the application itself, I focused on questions such as:

> What does this application need to run?

> Where should its dependencies be installed?

> Which files need to be inside the final image?

> What should happen during the build stage versus the runtime stage?

> Which user should the application run as?

> Where are files located inside each Docker stage?

These questions helped me move beyond simply memorizing Docker commands and start understanding **why each Dockerfile instruction is being used**.

---

## Scope & Transparency

To be transparent:

**I did not write the Python application or implement the rate-limiting logic.**

The application was provided as a learning exercise.

My contribution was creating the Dockerfile and using the project to practice my understanding of **Docker containerization, multi-stage builds, dependencies, file paths, permissions, and non-root execution.**

I believe documenting this distinction is important because the purpose of this project is to demonstrate my **Docker learning and hands-on containerization practice**, rather than claim ownership of application development that I did not perform.

---

## Next Steps

As I continue developing my Docker skills, I plan to build on this knowledge by practicing:

* Docker networking
* Volumes and persistent data
* Docker Compose
* Image optimization
* Build caching
* Container security
* Container registries
* AWS container services such as Amazon ECR and ECS

---

## About This Project

This project is part of my hands-on journey toward becoming a **Cloud / Cloud Infrastructure Engineer**, with a focus on developing practical skills in Docker, AWS, infrastructure, and cloud technologies.

