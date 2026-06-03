# Project Context — Itinerario-base-zamudia

## Stack
- Flask, PyMySQL (no SQLAlchemy), Flask-Login, Flask-SocketIO, Flask-WTF
- Dual DB: `estadio_db` (funcional) + `no_funcional` (usuarios, roles, bitácora) — same MySQL server
- Templates: Jinja2 (vanilla, no JS framework)

## Architecture (migrated from SQLAlchemy ORM → raw SQL PDO-style)
- **Entities** (`app/models/`): POPO classes with `**kwargs` **last** in `__init__` so SQL JOIN columns override Python defaults.
  - `self.atributo = default` explícito antes del `**kwargs` loop.
- **Repositories** (`app/repositories/`): Only layer that executes SQL. 3 core methods via `BaseRepository`: `fetch_all`, `fetch_one`, `execute`. Auto-commit on single statements; explicit `commit()/rollback()` for transactions.
- **Services** (`app/services/`): Business logic, no SQL.
- **Controllers** (`app/controllers/`): Classes with dependency injection (repo/service via `__init__`).
- **Routes** (`app/routes/`): Blueprints mapping URL → controller method.
- **DatabaseManager** (`app/database/connection.py`): Flask `g` object per request, `teardown_appcontext` for cleanup.

## Key Patterns
- `@permiso_requerido(codigo)` decorator on routes.
- `Usuario.tiene_permiso(codigo)` caches permisos via `UNION` SQL + `_permisos_cache`.
- Dual DB: cross-DB joins handled in repositories via `UsuarioRepository` calls.
- Blueprint `en_vivo` is CSRF-exempt (SocketIO manages its own security).
- `regenerar_permisos_por_rol()` avoids infinite recursion by calling `self.__class__` methods.

## Modules (9 blueprints, 46 routes)
1. auth    2. dashboard  3. usuario  4. rol  5. guion
6. en_vivo 7. mantenimiento  8. premio  9. bitacora

## Known Issues / Gotchas
- `Entities.__init__`: kwargs MUST go last, explicit attributes first. If a JOIN column name matches an attribute, kwargs override ensures it works.
- `BaseRepository.execute()` auto-commits. For multi-step transactions, call `self.commit()`/`self.rollback()` explicitly.
- `run.py` runs via `python3 run.py` (not `flask run`) — starts Flask + SocketIO in one process.
- No migration tool — schema is `estadio_db.sql` + `no_funcional.sql`.

## Recent Work (complete)
- Full SQLAlchemy → raw SQL migration (Phases 0–7), all entities, repos, controllers, routes rewritten.
- Fixed kwargs ordering bugs in 6 entity files.
- Deleted old ORM model files (`*_model.py`, `interfaces.py`).
- Replaced `ARQUITECTURA_DEL_SISTEMA.md` with full 900+ line document.
- Added `ultimo_acceso` column to `no_funcional.usuarios` (was missing from schema).

## Entry Point
- `app/__init__.py` → `create_app()` factory.
- `python3 run.py` to start.
