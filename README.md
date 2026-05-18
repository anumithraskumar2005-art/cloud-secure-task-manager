# Cloud-Based Secure Task Manager

A secure task management web application built as a DevSecOps capstone project. The project demonstrates application development, cybersecurity, Docker containerization, cloud deployment planning, monitoring, and logging.

## Project Objective

The objective of this project is to design, build, secure, deploy, and monitor a cloud-based web application using DevSecOps best practices.

## Features

- User registration and login
- Password hashing using bcrypt
- Role-based access control for User and Admin
- Task CRUD operations
- Task attachment upload
- Admin dashboard
- Login activity logs
- Failed login tracking
- Rate limiting for login protection
- Security headers
- Health check endpoint
- Dockerized application

## Tech Stack

- Python Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-Limiter
- SQLite for local development
- Docker
- GitHub
- AWS deployment planned with EC2, RDS, S3, VPC, Security Groups, and CloudWatch

## Security Features

- Passwords are stored as bcrypt hashes
- Role-based authorization protects admin routes
- Login attempts are recorded
- Rate limiting protects against brute-force attacks
- Security headers are added to HTTP responses
- SQL injection risk is reduced using SQLAlchemy ORM
- File uploads are restricted by allowed file types

## DevOps Features

- Source code managed using Git and GitHub
- Application containerized using Docker
- Docker Compose configuration included
- Health endpoint available at `/health`
- Project ready for CI/CD pipeline integration

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/anumithraskumar2005-art/cloud-secure-task-manager.git
cd cloud-secure-task-manager
