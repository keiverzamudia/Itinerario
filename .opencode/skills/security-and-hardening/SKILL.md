---
name: security-and-hardening
description: Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services. Use when personal data or privacy compliance (GDPR, CCPA) is involved.
---

# Security and Hardening

## Overview

Security-first development practices for web applications. Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory. Security isn't a phase — it's a constraint on every line of code that touches user data, authentication, or external systems.

## When to Use

- Building anything that accepts user input
- Implementing authentication or authorization
- Storing or transmitting sensitive data
- Integrating with external APIs or services
- Adding file uploads, webhooks, or callbacks
- Handling payment or PII data

## Process: Threat Model First

Controls bolted on without a threat model are guesses. Before hardening, spend five minutes thinking like an attacker:

1. **Map the trust boundaries.** Where does untrusted data cross into your system? HTTP requests, form fields, file uploads, webhooks, third-party APIs, message queues. Every boundary is attack surface.
2. **Name the assets.** What's worth stealing or breaking? Credentials, PII, payment data, admin actions, money movement.
3. **Run STRIDE over each boundary:**

| Threat | Ask | Typical mitigation |
|---|---|---|
| **S**poofing | Can someone impersonate a user/service? | Authentication, signature verification |
| **T**ampering | Can data be altered in transit or at rest? | Integrity checks, parameterized queries, HTTPS |
| **R**epudiation | Can an action be denied later? | Audit logging of security events |
| **I**nformation disclosure | Can data leak? | Encryption, field allowlists, generic errors |
| **D**enial of service | Can it be overwhelmed? | Rate limiting, input size caps, timeouts |
| **E**levation of privilege | Can a user gain rights they shouldn't? | Authorization checks, least privilege |

4. **Write abuse cases next to use cases.** For each feature, ask "how would I misuse this?" — then make that your first test.

## The Three-Tier Boundary System

### Always Do (No Exceptions)

- **Validate all external input** at the system boundary (API routes, form handlers)
- **Parameterize all database queries** — never concatenate user input into SQL
- **Encode output** to prevent XSS (use framework auto-escaping, don't bypass it)
- **Use HTTPS** for all external communication
- **Hash passwords** with bcrypt/scrypt/argon2 (never store plaintext)
- **Set security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- **Use httpOnly, secure, sameSite cookies** for sessions

### Ask First (Requires Human Approval)

- Adding new authentication flows or changing auth logic
- Storing new categories of sensitive data (PII, payment info)
- Adding new external service integrations
- Changing CORS configuration
- Adding file upload handlers
- Modifying rate limiting or throttling
- Granting elevated permissions or roles

### Never Do

- **Never commit secrets** to version control (API keys, passwords, tokens)
- **Never log sensitive data** (passwords, tokens, full credit card numbers)
- **Never trust client-side validation** as a security boundary
- **Never disable security headers** for convenience
- **Never use `eval()` or `innerHTML`** with user-provided data
- **Never store sessions in client-accessible storage** (localStorage for auth tokens)
- **Never expose stack traces** or internal error details to users

## OWASP Top 10 Prevention Patterns

### Injection (SQL, NoSQL, OS Command)

```python
# BAD: SQL injection via string concatenation
query = f"SELECT * FROM users WHERE id = '{user_id}'"

# GOOD: Parameterized query
cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Broken Authentication

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Password hashing
hashed = generate_password_hash(plaintext, method='scrypt', salt_length=16)
is_valid = check_password_hash(hashed, plaintext)
```

### Cross-Site Scripting (XSS)

```html
<!-- BAD: Rendering user input as HTML -->
<div>{{ user_input | safe }}</div>

<!-- GOOD: Auto-escaping (default in Jinja2) -->
<div>{{ user_input }}</div>

<!-- GOOD: tojson for JavaScript contexts -->
<script>const data = {{ data | tojson }};</script>
```

### Broken Access Control

```python
# Always check authorization, not just authentication
@bp.route('/api/tasks/<int:id>', methods=['PATCH'])
@permiso_requerido('gestion_tarea.edit')
def update_task(id):
    task = TaskModel.obtener_por_id(id)
    if task['creado_por'] != current_user.id:
        return jsonify({'error': 'Forbidden'}), 403
```

### Security Misconfiguration

```python
# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### Sensitive Data Exposure

```python
# Never return sensitive fields in API responses
def sanitize_user(user):
    return {k: v for k, v in user.items() if k != 'password_hash'}
```

## Input Validation Patterns

### Schema Validation at Boundaries

```python
# Validate at the route handler
@bp.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title'}), 422
    if len(data['title']) > 200:
        return jsonify({'error': 'Title too long'}), 422
```

### File Upload Safety

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

def validate_upload(file):
    if file.filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError('File type not allowed')
    if file.content_length > MAX_SIZE:
        raise ValidationError('File too large')
```

## Security Review Checklist

### Authentication
- [ ] Passwords hashed with werkzeug scrypt
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Password reset tokens expire

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] Users can only access their own resources
- [ ] Admin actions require admin role verification

### Input
- [ ] All user input validated at the boundary
- [ ] SQL queries are parameterized
- [ ] HTML output is encoded/escaped

### Data
- [ ] No secrets in code or version control
- [ ] Sensitive fields excluded from API responses

### Infrastructure
- [ ] Security headers configured
- [ ] CORS restricted to known origins
- [ ] Error messages don't expose internals

## Red Flags

- User input passed directly to database queries, shell commands, or HTML rendering
- Secrets in source code or commit history
- API endpoints without authentication or authorization checks
- Missing CORS configuration or wildcard (`*`) origins
- No rate limiting on authentication endpoints
- Stack traces or internal errors exposed to users
