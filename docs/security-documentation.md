# Security Documentation

## Project Name

Cloud-Based Secure Task Manager

## Objective

This document explains the security features implemented in the Secure Task Manager web application. The project follows DevSecOps principles by integrating security into application development, deployment, monitoring, and documentation.

---

## 1. Authentication Security

The application includes user registration and login functionality.

### Implementation

- Users register with name, email, and password.
- Email is used as the unique login identity.
- Users must login before accessing the dashboard.
- Unauthorized users are redirected to the login page.
- Flask-Login is used to manage authenticated sessions.

### Related Feature

```text
User Registration
User Login
Protected Dashboard
Logout
```

---

## 2. Password Hashing

Plain text passwords are not stored in the database.

### Implementation

The application uses bcrypt to hash passwords before storing them.

```python
password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
```

During login, the entered password is compared with the stored hash:

```python
bcrypt.check_password_hash(user.password_hash, password)
```

### Security Benefit

Even if the database is exposed, original user passwords cannot be directly read.

---

## 3. Role-Based Access Control

The application supports two roles:

```text
user
admin
```

### User Role

A normal user can:

- Login
- Create tasks
- View own tasks
- Edit own tasks
- Delete own tasks
- Upload task attachments

### Admin Role

An admin can:

- Access the admin dashboard
- View registered users
- View all tasks
- View login logs
- Monitor failed login attempts

### Implementation

Admin routes are protected using role checking:

```python
if current_user.role != "admin":
    flash("Access denied. Admins only.", "danger")
    return redirect(url_for("main.dashboard"))
```

### Security Benefit

Normal users cannot access admin-only pages or sensitive dashboard information.

---

## 4. Brute-Force Protection and Rate Limiting

The login route is protected using Flask-Limiter.

### Implementation

```python
@limiter.limit("5 per minute")
```

### Security Benefit

Rate limiting helps reduce brute-force attacks by limiting repeated login attempts.

---

## 5. Login Activity Logging

The application records login activity.

### Logged Information

```text
Email
IP address
Login status
Timestamp
```

### Login Status Values

```text
success
failed
```

### Security Benefit

Admins can monitor suspicious login behavior from the admin dashboard.

---

## 6. SQL Injection Prevention

The application uses SQLAlchemy ORM instead of raw SQL queries.

### Example

```python
User.query.filter_by(email=email).first()
```

### Security Benefit

Using ORM queries reduces SQL injection risk because database operations are handled through structured query methods instead of unsafe string concatenation.

---

## 7. Cross-Site Scripting Protection

The application uses Flask Jinja templates, which escape output by default.

### Example

```html
{{ task.title }}
{{ task.description }}
```

### Example Task Used For Testing

```text
Title:
AWS Cloud Infrastructure Setup

Description:
Design and configure a secure AWS environment with VPC, public and private subnets, EC2, RDS, S3, Security Groups, and CloudWatch monitoring for the Secure Task Manager application.
```

### Security Benefit

Escaping user-controlled output reduces the risk of cross-site scripting attacks.

---

## 8. Security Headers

The application adds security headers to HTTP responses.

### Implemented Headers

```text
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'
```

### Security Benefit

These headers help protect against:

- Clickjacking
- MIME sniffing
- Unsafe referrer leakage
- Some cross-site scripting risks

---

## 9. Secure File Upload

The application supports task attachment upload.

### Allowed File Types

```text
png
jpg
jpeg
pdf
docx
txt
```

### Implementation

Uploaded file names are sanitized using:

```python
secure_filename(uploaded_file.filename)
```

### Security Benefit

Restricting file types and sanitizing file names reduces upload-related security risks.

---

## 10. Health Check Endpoint

The application provides a health check endpoint.

### Endpoint

```text
/health
```

### Expected Response

```json
{
  "database": "connected",
  "service": "secure-task-manager",
  "status": "ok"
}
```

### Security and Monitoring Benefit

The health check endpoint can be used by monitoring tools, Docker checks, AWS CloudWatch, or an Application Load Balancer health check.

---

## 11. Docker Security Considerations

The application is containerized using Docker.

### Benefits

- Provides a consistent runtime environment
- Helps isolate application dependencies
- Makes deployment easier
- Supports CI/CD automation

### Future Production Improvements

For production deployment:

- Use Gunicorn instead of Flask development server
- Use a non-root Docker user
- Scan Docker images using tools like Trivy or Snyk
- Store secrets using environment variables or AWS Secrets Manager

---

## 12. AWS Security Plan

During AWS deployment, the following security measures are planned.

### VPC Security

- Use a custom VPC
- Use public and private subnets
- Place RDS in a private subnet
- Use Security Groups with least privilege access

### EC2 Security

- Allow SSH only from a trusted IP
- Disable root login
- Disable password authentication
- Enable UFW firewall
- Enable fail2ban

### RDS Security

- Disable public access
- Allow database access only from EC2 Security Group
- Enable automated backups

### S3 Security

- Block public access
- Enable encryption
- Enable versioning
- Store uploads and backups securely

### Monitoring Security

- Send logs to CloudWatch
- Track failed login attempts
- Configure alarms for suspicious activity

---

## 13. HTTPS Plan

For production deployment, HTTPS will be configured using one of the following methods:

```text
AWS ACM with Application Load Balancer
```

or:

```text
Let's Encrypt with Nginx
```

### Security Benefit

HTTPS protects data in transit between the user browser and the application.

---

## 14. Security Testing Checklist

Before final submission, verify the following:

- Passwords are stored as bcrypt hashes
- Normal users cannot access `/admin`
- Admin dashboard is protected
- Login rate limiting works
- Failed login attempts appear in login logs
- SQLAlchemy ORM is used for database operations
- Uploaded file types are restricted
- Security headers are added
- `/health` endpoint works
- Docker container runs successfully
- GitHub Actions workflow passes

---

## Conclusion

The Secure Task Manager project implements important DevSecOps security practices including password hashing, role-based access control, login monitoring, rate limiting, secure file upload, security headers, Dockerization, health checks, and AWS security planning. These measures improve confidentiality, integrity, availability, and operational visibility of the application.
