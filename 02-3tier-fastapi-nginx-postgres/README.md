# 3-Tier Web Application Stack (Nginx + FastAPI + PostgreSQL)

This project demonstrates a classic 3-tier architecture used in production systems.

Stack:

- Nginx — reverse proxy
- FastAPI — backend application
- PostgreSQL — database
- Docker Compose — orchestration
- Docker networks — network isolation
- Healthchecks — service readiness verification

---

# Architecture

Client → Nginx → Backend → Database

Docker networks:

front network:
- nginx
- backend

back network:
- backend
- database

Database is NOT accessible from the front network directly.

This improves security.

---

# Reverse proxy purpose

Nginx:

- hides backend from direct internet access
- provides single entry point
- allows TLS termination
- allows load balancing
- allows security headers

---

# Health endpoints

/health  
Checks backend process is running.

Example:

curl http://localhost:8080/health

Response:

{"status":"ok"}


/ready  
Checks backend can connect to database.

Example:

curl http://localhost:8080/ready

Response:

{"status":"ready"}

If database unavailable:

{"status":"not ready"}

---

# Docker healthchecks

Check container status:

docker ps

Example:

t3-backend   Up (healthy)  
t3-db        Up (healthy)  
t3-nginx     Up  

---

# Run project

cd 02-3tier-fastapi-nginx-postgres

cp .env.example .env

docker compose up -d --build

---

# Test

curl http://localhost:8080/health

curl http://localhost:8080/ready

curl http://localhost:8080/db

---

# Stop

docker compose down

Remove volumes:

docker compose down -v

---

# Project demonstrates

- Docker networking
- Network isolation
- Reverse proxy configuration
- Backend‑database connectivity
- Healthchecks
- Infrastructure as code

---

# Technologies

Docker  
Docker Compose  
Nginx  
FastAPI  
PostgreSQL  

---

DevOps learning project.
