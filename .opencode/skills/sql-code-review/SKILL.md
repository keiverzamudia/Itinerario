---
name: sql-code-review
description: Review SQL queries and database access patterns for security, performance, and correctness. Use when writing or modifying SQL queries, models, database helpers, or when reviewing code that touches the database. Trigger words: "SQL review", "query review", "database review", "N+1", "índice", "transacción".
---

# SQL Code Review

Review SQL queries and database access patterns for security, performance, and correctness. Tailored for PyMySQL (raw SQL, no ORM) with MySQL.

## Security

### Injection Prevention

```python
# ❌ SQL injection via string concatenation
query = f"SELECT * FROM users WHERE id = '{user_id}'"

# ❌ SQL injection via format
query = "SELECT * FROM users WHERE id = '{}'".format(user_id)

# ✅ Parameterized query
cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**Rules:**
- Only `%s` with tuple in PyMySQL
- No f-strings, format, or `+` with values in SQL
- Identifiers (column/table names) go by whitelist, never from user input

### Access Control

- Every query that modifies data must be preceded by permission check
- Users should only access their own data (IDOR prevention)
- Password hashes must never be exposed in query results

## Performance

### N+1 Queries

The most common performance anti-pattern: executing 1 query per item in a loop.

```python
# ❌ N+1: 1 query per user
for uid in user_ids:
    user = cur.execute("SELECT * FROM usuarios WHERE id = %s", (uid,))

# ✅ Batch query
placeholders = ', '.join(['%s'] * len(user_ids))
cur.execute(f"SELECT id, nombre FROM usuarios WHERE id IN ({placeholders})", user_ids)
```

### Missing Indexes

Before adding an index, verify the query actually needs one:
- Is the column in a WHERE clause?
- Is it in a JOIN condition?
- Is it in an ORDER BY?

```sql
-- Verify index usage
EXPLAIN SELECT * FROM guiones WHERE estado = 'en_vivo';
```

### SELECT * Anti-pattern

```python
# ❌ Exposes all columns including password_hash
cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))

# ✅ Explicit column list
cur.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id,))
```

### Missing LIMIT

```python
# ❌ Unbounded query on growing table
cur.execute("SELECT * FROM actividad_usuario ORDER BY created_at DESC")

# ✅ Bounded query
cur.execute("SELECT * FROM actividad_usuario ORDER BY created_at DESC LIMIT 500")
```

## Correctness

### Transaction Requirements

```python
# ❌ Two writes without transaction — partial failure possible
cur.execute("DELETE FROM videos WHERE reel_id = %s", (id,))
cur.execute("DELETE FROM reels WHERE id = %s", (id,))

# ✅ Transaction
with transaction() as cur:
    cur.execute("DELETE FROM videos WHERE reel_id = %s", (id,))
    cur.execute("DELETE FROM reels WHERE id = %s", (id,))
```

**Rule:** Any multi-statement write MUST use `with transaction():`.

### NULL vs Empty String

```python
# ❌ Empty string for missing data
cur.execute("UPDATE users SET phone = '' WHERE id = %s", (id,))

# ✅ Explicit NULL
cur.execute("UPDATE users SET phone = NULL WHERE id = %s", (id,))
```

### JOIN Missing

```python
# ❌ Two separate queries + Python join
users = cur.execute("SELECT * FROM usuarios")
for u in users:
    u['rol'] = cur.execute("SELECT * FROM roles WHERE id = %s", (u['rol_id'],))

# ✅ SQL JOIN
cur.execute("""
    SELECT u.*, r.nombre as rol_nombre
    FROM usuarios u
    JOIN roles r ON u.rol_id = r.id
""")
```

## Review Checklist

- [ ] All queries use `%s` parameterized placeholders
- [ ] No SELECT * (explicit columns)
- [ ] Multi-statement writes use `transaction()`
- [ ] No N+1 query patterns
- [ ] Queries that grow unbounded have LIMIT
- [ ] JOINs used instead of Python-side loops
- [ ] Password hashes never exposed in results
- [ ] Indexes exist for WHERE/JOIN/ORDER BY columns
