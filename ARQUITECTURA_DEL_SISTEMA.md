# Arquitectura del Sistema — Itinerario Estadio

## Índice

1. [Visión General](#1-visión-general)
2. [Estructura del Proyecto](#2-estructura-del-proyecto)
3. [Arquitectura de Bases de Datos](#3-arquitectura-de-bases-de-datos)
4. [Capas del Sistema](#4-capas-del-sistema)
5. [Sistema de Roles y Permisos](#5-sistema-de-roles-y-permisos)
6. [Módulo Auth (Login/Logout)](#6-módulo-auth-loginlogout)
7. [Módulo Bitácora (Auditoría)](#7-módulo-bitácora-auditoría)
8. [Módulo Dashboard + SocketIO](#8-módulo-dashboard--socketio)
9. [Módulo Guión + En Vivo](#9-módulo-guión--en-vivo)
10. [Módulo Mantenimiento](#10-módulo-mantenimiento)
11. [Módulo Premios](#11-módulo-premios)
12. [Módulo Usuarios](#12-módulo-usuarios)
13. [Cómo Crear un Módulo desde Cero](#13-cómo-crear-un-módulo-desde-cero)
14. [Principios SOLID Aplicados](#14-principios-solid-aplicados)
15. [Patrones de Diseño Usados](#15-patrones-de-diseño-usados)
16. [Apéndice](#16-apéndice)

---

## 1. Visión General

Sistema web para gestión de estadio (Itinerario) con autenticación, roles, permisos, guión en vivo, mantenimiento de recursos, premios y bitácora de auditoría. Construido con Python/Flask + MySQL nativo (sin ORM).

### Tech Stack

| Componente | Versión | Propósito |
|---|---|---|
| Python | 3.14+ | Lenguaje base |
| Flask | 3.x | Framework web (microframework) |
| Flask-Login | — | Manejo de sesiones de usuario |
| Flask-WTF | — | CSRF + formularios WTForms |
| Flask-SocketIO | 5.x | WebSocket para guión en vivo |
| PyMySQL | 1.x | Conector MySQL (driver nativo) |
| MySQL | 8.x | Motor de base de datos |
| Bootstrap | 5 | UI/Frontend |
| SweetAlert2 | — | Alertas JS modernas |

### Filosofía de Diseño

- **Sin ORM**: Todo el acceso a datos es SQL nativo con placeholders `%s` (estilo PDO de PHP). Cada repositorio es dueño de sus consultas.
- **POPO Entities**: Los modelos son clases Python planas (Plain Old Python Objects) sin herencia de framework. Solo transportan datos.
- **Capa única de SQL**: Solo los repositorios ejecutan consultas. Ni servicios, ni controladores, ni helpers tocan la base de datos directamente.
- **Dual DB**: Dos bases de datos MySQL independientes separan datos funcionales (`estadio_db`) de datos no funcionales (`no_funcional`: usuarios, roles, bitácora).
- **Controllers como clases**: Cada controlador es una clase con dependencias inyectadas en `__init__`. Las rutas están en archivos separados (`app/routes/`).
- **Auditoría completa**: Toda operación CRUD queda registrada automáticamente en la bitácora con trazabilidad de quién, cuándo, qué cambió (antes/después).

### Mapa de Dependencias entre Módulos

```
auth ←────── usuarios (no_funcional)
  │
  ├── dashboard ←── guión (en vivo) + SocketIO
  │
  ├── guion ←────── usuarios (encargado)
  │     │
  │     └── en_vivo ←── SocketIO
  │
  ├── mantenimiento ←── usuarios (cross-DB)
  │
  ├── premios ←── patrocinadores
  │
  ├── roles ←────── usuarios + permisos
  │
  └── bitácora ←── usuarios (toda actividad)
```

Cada módulo tiene su propia estructura de 4 carpetas (modelos, repositorios, controladores, rutas).

---

## 2. Estructura del Proyecto

### 2.1 Árbol de Directorios

```
Itinerario-base-zamudia/
├── run.py                           ← Punto de entrada único
├── requirements.txt                 ← Dependencias pip
├── crear_admin.py                   ← Seed de Superadmin inicial
├── migrar_a_dual_db.py              ← Script de migración histórica
├── estadio_db.sql                   ← Esquema BD funcional
├── no_funcional.sql                 ← Esquema BD no funcional
├── ARQUITECTURA_DEL_SISTEMA.md      ← Este documento
│
└── app/
    ├── __init__.py                  ← Fábrica Flask (create_app)
    │                                  Conexiones: g object → teardown
    │                                  Login manager + user_loader
    │                                  Seed automático de permisos
    │                                  Registro de blueprints
    │                                  Eventos SocketIO globales
    │
    ├── config.py                    ← DATABASE_CONFIG (2 conexiones)
    │                                  UPLOAD_FOLDER, ALLOWED_EXTENSIONS
    │
    ├── database/
    │   ├── __init__.py
    │   └── connection.py            ← DatabaseManager
    │                                  get_connection(db_name) → pymysql conn
    │                                  init_app(app) → teardown_appcontext
    │
    ├── models/                      ← Entidades POPO (solo datos)
    │   ├── __init__.py
    │   ├── usuario.py               ← Usuario (con Flask-Login methods)
    │   ├── rol.py                   ← Rol, Permiso, RolPermiso, UsuarioPermiso
    │   ├── guion.py                 ← Guion, GuionFecha, ElementoGuion
    │   ├── mantenimiento.py         ← Recurso, Mantenimiento, HistorialMantenimiento
    │   ├── premio.py                ← Premio, Patrocinador
    │   ├── bitacora.py              ← SesionUsuario, ActividadUsuario,
    │                                   CambioPorModulo, ErrorAplicacion
    │   └── models.py                ← Departamento, Evento, Sincronizacion (itinerario)
    │
    ├── repositories/                ← ÚNICO lugar con SQL nativo
    │   ├── __init__.py
    │   ├── base_repository.py       ← BaseRepository (fetch_all, fetch_one, execute)
    │   ├── usuario_repository.py
    │   ├── rol_repository.py        ← RolRepository + PermisoRepository
    │   │                              + RolPermisoRepository + UsuarioPermisoRepository
    │   ├── guion_repository.py      ← GuionRepository + ElementoGuionRepository
    │   ├── mantenimiento_repository.py ← RecursoRepository + MantenimientoRepository
    │   ├── premio_repository.py
    │   ├── en_vivo_repository.py
    │   └── bitacora_repository.py   ← SesionRepository + ActividadRepository
    │                                  + CambioRepository + ErrorRepository
    │
    ├── services/                    ← Lógica de negocio (orquestación)
    │   ├── __init__.py
    │   ├── rol_service.py           ← Seed permisos, dashboard roles, CRUD
    │   ├── guion_service.py         ← Validaciones de elementos, publicación
    │   ├── en_vivo_service.py       ← Control de estado en vivo
    │   ├── premio_service.py        ← CRUD + entrega de premios
    │   └── bitacora_service.py      ← Sesiones, actividad, cambios, errores
    │
    ├── controllers/                 ← Clases que manejan HTTP (request → response)
    │   ├── __init__.py
    │   ├── auth_controller.py       ← AuthController
    │   ├── dashboard_controller.py  ← DashboardController
    │   ├── guion_controller.py      ← GuionController
    │   ├── en_vivo_controller.py    ← EnVivoController
    │   ├── mantenimiento_controller.py ← MantenimientoController
    │   ├── premio_controller.py     ← PremioController
    │   ├── usuario_controller.py    ← UsuarioController
    │   ├── rol_controller.py        ← RolController
    │   └── bitacora_controller.py   ← BitacoraController
    │
    ├── routes/                      ← Solo mapeo URL → método del controller
    │   ├── __init__.py
    │   ├── auth_routes.py
    │   ├── dashboard_routes.py
    │   ├── guion_routes.py
    │   ├── en_vivo_routes.py
    │   ├── mantenimiento_routes.py
    │   ├── premio_routes.py
    │   ├── usuario_routes.py
    │   ├── rol_routes.py
    │   └── bitacora_routes.py
    │
    ├── forms/                       ← Formularios Flask-WTF
    │   ├── auth_form.py
    │   ├── guion_form.py
    │   ├── usuario_form.py
    │   ├── mantemiento_form.py
    │   ├── premio_form.py
    │   └── rol_form.py
    │
    ├── helpers/                     ← Utilidades transversales
    │   ├── decorators.py            ← @permiso_requerido
    │   └── bitacora_helper.py       ← Helper contextual para bitácora
    │
    ├── traits/
    │   └── validaciones.py          ← ValidacionesMixin (como trait PHP)
    │
    ├── templates/                   ← Jinja2 (sin cambios estructurales)
    └── static/                      ← CSS, JS, imágenes
```

### 2.2 Mapa de Blueprints y Rutas

| Blueprint | URL Prefix | Archivo routes/ | Rutas principales |
|---|---|---|---|
| `auth` | `/auth` | `auth_routes.py` | `/login`, `/logout` |
| `dashboard` | `/` | `dashboard_routes.py` | `/dashboard` |
| `guion` | `/guiones` | `guion_routes.py` | `/`, `/crear`, `/agregar-elemento/<id>`, `/publicar/<id>`, `/eliminar/<id>` |
| `en_vivo` | `/en-vivo` | `en_vivo_routes.py` | `/`, `/<id>`, `/iniciar/<id>`, `/finalizar/<id>` |
| `mantenimiento` | `/mantenimiento` | `mantenimiento_routes.py` | `/`, `/recursos/crear`, `/ingresar/<id>`, `/ver/<id>`, `/reparar/<id>` |
| `premio` | `/premios` | `premio_routes.py` | `/`, `/eliminar/<id>` |
| `usuario` | `/usuarios` | `usuario_routes.py` | `/`, `/crear`, `/editar/<id>`, `/eliminar/<id>`, `/perfil` |
| `rol` | `/roles` | `rol_routes.py` | `/`, `/crear`, `/editar/<id>`, `/editar-rol/<id>` |
| `bitacora` | `/bitacora` | `bitacora_routes.py` | `/`, `/usuario/<id>` |

### 2.3 Flujo de una Petición

```
Navegador → HTTP Request
    │
    ▼
[Flask-WTF CSRF Protection] (POST/ PUT/ DELETE)
    │
    ▼
[Flask-Login] (current_user → ¿autenticado?)
    │
    ▼
[@permiso_requerido] (current_user.tiene_permiso('x.y')?)
    │
    ▼
Route (app/routes/X_routes.py)
    │  llama al método del Controller
    ▼
Controller (app/controllers/X_controller.py :: Clase)
    │  Recibe request, crea forms, llama Service
    │  NO ejecuta SQL directamente
    ▼
Service (app/services/X_service.py)
    │  Valida (ValidacionesMixin), orquesta repos, decide flujo
    │  NO ejecuta SQL directamente
    ▼
Repository (app/repositories/X_repository.py)
    │  Ejecuta SQL nativo con pymysql + %s placeholders
    │  Retorna entidades POPO (o listas de ellas)
    ▼
[BitacoraHelper.registrar_actividad] (si aplica)
    │
    ▼
Controller renderiza template (Jinja2) o redirige
```

## 3. Arquitectura de Bases de Datos

### 3.1 Estrategia Dual DB

El sistema usa **dos bases de datos MySQL independientes** en el mismo servidor:

```
┌──────────────────────────────────┐     ┌──────────────────────────────────┐
│         estadio_db               │     │         no_funcional             │
│      (Base funcional)            │     │     (Base no funcional)          │
├──────────────────────────────────┤     ├──────────────────────────────────┤
│ departamentos                    │     │ usuarios                         │
│ eventos                          │     │ roles                            │
│ sincronizaciones                 │     │ permisos                         │
│ eventos_sincronizados            │     │ rol_permiso                      │
│ guiones                          │     │ usuario_permiso                  │
│ guion_fechas                     │     │ sesiones_usuario                 │
│ elementos_guion                  │     │ actividad_usuario                │
│ patrocinadores                   │     │ cambios_por_modulo               │
│ premios                          │     │ errores_aplicacion               │
│ recursos                         │     │                                  │
│ mantenimientos                   │     │                                  │
│ historial_mantenimiento          │     │                                  │
└──────────────────────────────────┘     └──────────────────────────────────┘
     │                                           │
     └────────── Mismo servidor MySQL ───────────┘
```

**¿Por qué dos bases?**
- **Seguridad**: Los datos de autenticación (passwords, roles, permisos) están aislados de los datos funcionales del estadio.
- **Escalabilidad**: Cada DB puede crecer, respaldarse y mantenerse independientemente.
- **Responsabilidad**: Si un módulo funcional tiene un bug, no puede corromper la tabla de usuarios.

### 3.2 DatabaseManager — Gestión de Conexiones

**Archivo**: `app/database/connection.py`

```python
from flask import g
from app.config import DATABASE_CONFIG

class DatabaseManager:
    @staticmethod
    def get_connection(db_name='estadio_db'):
        """Retorna una conexión pymysql por request (singleton por g)."""
        key = f'_db_{db_name}'
        if key not in g:
            cfg = DATABASE_CONFIG[db_name].copy()
            cfg['cursorclass'] = DictCursor  # ← Resultados como dicts
            g._db_connections[db_name] = pymysql.connect(**cfg)
            g._db_connections[db_name].autocommit(False)
        return g._db_connections[db_name]
```

**Claves de diseño**:
- **g object de Flask**: Cada request HTTP tiene su propio `g`. Las conexiones viven solo durante la request.
- **Singleton por request**: Si dos repositorios piden la misma DB, reciben la misma conexión (evita múltiples conexiones innecesarias).
- **autocommit(False)**: Todas las operaciones requieren `commit()` explícito. Si hay error, el `teardown_appcontext` hace `rollback()` automático.
- **DictCursor**: Los resultados vienen como diccionarios (`{'id': 1, 'nombre': 'X'}`), igual que `PDO::FETCH_ASSOC` en PHP.

**Ciclo de vida**:

```
Request llega
    │
    ▼
Repositorio A pide get_connection('estadio_db') → crea conexión
Repositorio B pide get_connection('estadio_db') → misma conexión
Repositorio C pide get_connection('no_funcional') → crea otra conexión
    │
    ▼
Request termina (éxito o error)
    │
    ▼
teardown_appcontext:
    ├── Si hubo error → rollback() en cada conexión
    └── Siempre → close() en cada conexión
```

### 3.3 Relaciones Cross-DB

No existen FK reales entre bases distintas (MySQL no lo permite). Las relaciones se manejan **a nivel de aplicación** mediante repositorios que hacen JOINs o consultas separadas.

**Ejemplo**: `Mantenimiento.usuario_id` apunta lógicamente a `no_funcional.usuarios.id`:

```python
# En el repositorio (mantenimiento_repository.py):
def _cargar_relaciones(self, m):
    # Carga el recurso (misma DB)
    recurso_row = self.fetch_one(
        "SELECT * FROM recursos WHERE id = %s", (m.recurso_id,)
    )
    # Carga el nombre del usuario (otra DB) — vía UsuarioRepository
    from app.repositories.usuario_repository import UsuarioRepository
    user = UsuarioRepository().obtener_por_id(m.usuario_id)
    m.usuario_nombre = user.nombre if user else None
```

**Tablas con referencias cross-DB**:

| Tabla (estadio_db) | Columna | Apunta a (no_funcional) |
|---|---|---|
| `mantenimientos` | `usuario_id` (INTEGER) | `usuarios.id` |
| `historial_mantenimiento` | `usuario_id` (INTEGER) | `usuarios.id` |
| `premios` | `entregado_por` (INTEGER) | `usuarios.id` |

### 3.4 Esquema `estadio_db`

```sql
departamentos:     id, nombre, descripcion, color
eventos:           id, titulo, descripcion, fecha, hora_inicio, hora_fin,
                   duracion_minutos, departamento_id (FK), estado, guion
sincronizaciones:  id, nombre, descripcion, fecha_sincronizacion,
                   hora_sincronizacion, estado
eventos_sincronizados: id, sincronizacion_id, evento_id, orden, ejecutado
guiones:           id, nombre, estado, creado_en, modificado_en
guion_fechas:      id, guion_id (FK), fecha
elementos_guion:   id, guion_id (FK), fecha_id, tipo, hora, inning,
                   medio_inning, contenido, duracion_estimada, encargado,
                   orden, estado
patrocinadores:    id_patrocinador, nombre_empresa
premios:           id, nombre, descripcion, id_patrocinador (FK), estado,
                   estatus, fecha_creacion, hora_creacion, foto,
                   fecha_entrega, entregado_por (INTEGER)
recursos:          id, nombre, descripcion, codigo (UNIQUE), ubicacion,
                   estado, creado_en, modificado_en
mantenimientos:    id, recurso_id (FK), usuario_id (INTEGER), estado,
                   fecha_ingreso, fecha_salida, diagnostico, observaciones,
                   creado_en
historial_mantenimiento: id, mantenimiento_id (FK), usuario_id (INTEGER),
                   accion, descripcion, creado_en
```

### 3.5 Esquema `no_funcional`

```sql
usuarios:          id, nombre, email (UNIQUE), cedula (UNIQUE), password_hash,
                   rol, departamento, telefono, activo, fecha_registro,
                   ultimo_acceso
roles:             id, nombre (UNIQUE), descripcion
permisos:          id, nombre, codigo (UNIQUE), modulo, descripcion
rol_permiso:       id, rol_id (FK), permiso_id (FK), UNIQUE(rol_id, permiso_id)
usuario_permiso:   id, usuario_id (FK), permiso_id (FK),
                   UNIQUE(usuario_id, permiso_id)

-- Bitácora:
sesiones_usuario:      id, usuario_id (FK), inicio_sesion, fin_sesion,
                       ip_address, user_agent, duracion_segundos
actividad_usuario:     id, sesion_id (FK), usuario_id (FK), tipo_accion,
                       modulo, accion, detalle (JSON), pagina, ip_address,
                       created_at
cambios_por_modulo:    id, actividad_id (FK), tabla_afectada, registro_id,
                       campo, valor_anterior, valor_nuevo, created_at
errores_aplicacion:    id, usuario_id (FK), tipo_error, mensaje, traceback,
                       pagina, ip_address, created_at
```

---

## 4. Capas del Sistema

### 4.1 Entities (POPO) — `app/models/`

**Propósito**: Solo transportar datos entre capas. Sin lógica de base de datos, sin herencia de framework.

**Patrón constructor**:

```python
class MiEntidad:
    def __init__(self, id=None, nombre=None, **kwargs):
        # 1. Propiedades fijas con valores por defecto explícitos
        self.id = id
        self.nombre = nombre
        self.propiedad_extra = None  # ← Se inicializa ANTES de kwargs
        # 2. kwargs al FINAL para absorber columnas de JOINs
        for k, v in kwargs.items():
            setattr(self, k, v)
```

**Regla de oro**: Las propiedades por defecto (como `self.usuario_nombre = None`) deben ir **antes** del bucle `kwargs` para que un JOIN de SQL pueda sobrescribirlas.

**Uso desde repositorios**:

```python
# El repositorio retorna entidades mapeadas desde SQL
return [MiEntidad(**row) for row in rows]  # ← Una línea: row es dict, **row lo expande
```

**Ventaja**: Si mañana agregas una columna en la BD o un JOIN extra, la entidad lo absorbe automáticamente sin cambiar el `__init__`.

### 4.2 BaseRepository — `app/repositories/base_repository.py`

**Propósito**: Clase base que todo repositorio debe heredar. Proporciona 4 métodos fundamentales.

```python
class BaseRepository:
    def __init__(self, db_name='estadio_db'):
        self.db_name = db_name  # ← ¿A qué DB conectarse?

    # Consulta que retorna VARIAS filas → list[dict]
    def fetch_all(self, sql, params=None):
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()

    # Consulta que retorna UNA fila → dict o None
    def fetch_one(self, sql, params=None):
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()

    # INSERT / UPDATE / DELETE → retorna lastrowid
    def execute(self, sql, params=None):
        with self._conn.cursor() as cur:
            cur.execute(sql, params or ())
            self._conn.commit()
            return cur.lastrowid

    # Para ejecutar múltiples INSERTs
    def execute_many(self, sql, params_list):
        with self._conn.cursor() as cur:
            cur.executemany(sql, params_list)
            self._conn.commit()
```

**Cómo usarlo en un repositorio específico**:

```python
class UsuarioRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')  # ← Esta repo trabaja en no_funcional

    def obtener_por_email(self, email):
        row = self.fetch_one(
            "SELECT * FROM usuarios WHERE email = %s", (email,)
        )
        return Usuario(**row) if row else None
```

### 4.3 Repositorios Específicos — `app/repositories/`

**Propósito**: Única capa que ejecuta SQL. Cada repositorio es dueño de las consultas de su módulo.

**Contrato mínimo** (no obligatorio, pero consistente):

| Método | SQL | Retorno |
|---|---|---|
| `consultar(**filtros)` | `SELECT ... WHERE ...` | `list[Entidad]` |
| `obtener_por_id(id)` | `SELECT ... WHERE id = %s` | `Entidad` o `None` |
| `registrar(datos)` | `INSERT INTO ...` | `Entidad` (la creada) |
| `modificar(id, datos)` | `UPDATE ... SET ... WHERE id = %s` | `Entidad` (la actualizada) |
| `eliminar(id)` | `DELETE FROM ... WHERE id = %s` | `bool` o nombre |

**Reglas**:
- TODO el SQL usa placeholders `%s`, nunca concatenación de strings.
- Los métodos retornan **entidades**, no dicts crudos (a menos que sea una API).
- Las relaciones se cargan explícitamente dentro del repositorio (ej: cargar `historial` dentro de `obtener_por_id` de mantenimiento).
- El commit se hace automáticamente en `execute()`. Para transacciones multi-paso, llamar `self.commit()` manual (ver `registrar_con_historial`).

### 4.4 Services — `app/services/`

**Propósito**: Orquestar lógica de negocio, validaciones y reglas compuestas que involucran múltiples repositorios.

```python
class MiServicio(ValidacionesMixin):
    def __init__(self):
        self.repo = MiRepositorio()
        self.otro_repo = OtroRepositorio()

    def hacer_algo(self, datos):
        self.limpiar_errores()
        self.validar_obligatorios(['campo1'], datos)
        if self.tiene_errores():
            return None
        # Lógica de negocio
        return self.repo.registrar(datos)
```

**Reglas**:
- Los servicios **no ejecutan SQL** directamente.
- Los servicios pueden orquestar múltiples repositorios.
- Las validaciones se delegan al `ValidacionesMixin`.
- Los servicios retornan entidades, dicts o `None` (con errores accesibles vía `get_errores()`).

### 4.5 Controllers — `app/controllers/`

**Propósito**: Manejar la interacción HTTP (request → response). Son clases con dependencias inyectadas en `__init__`.

```python
class MiController:
    def __init__(self):
        self.service = MiServicio()  # ← Dependencia inyectada

    def listar(self):
        datos = self.service.obtener_todo()
        return render_template('modulo/lista.html', **datos)

    def crear(self):
        form = MiFormulario()
        if form.validate_on_submit():
            resultado = self.service.hacer_algo(form.data)
            if resultado:
                flash('Creado', 'success')
                return redirect(url_for('mi_modulo.listar'))
        return render_template('modulo/crear.html', form=form)
```

**Reglas**:
- No ejecutan SQL directamente.
- No contienen lógica de negocio compleja (eso es del Service).
- Manejan `request`, `session`, `flash`, `render_template`, `redirect`.
- Llaman a `bitacora_helper.registrar_actividad()` después de operaciones exitosas.

### 4.6 Routes — `app/routes/`

**Propósito**: Única responsabilidad: mapear URLs a métodos del controller.

```python
# app/routes/mi_modulo_routes.py
from flask import Blueprint
from app.controllers.mi_controller import MiController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('mi_modulo', __name__, url_prefix='/mi-modulo')
controller = MiController()

bp.route('/')(login_required(permiso_requerido('mi_modulo.view')(controller.listar)))
bp.route('/crear', methods=['GET', 'POST'])(
    login_required(permiso_requerido('mi_modulo.create')(controller.crear))
)
```

**Patrón de seguridad**: Cada ruta envuelve el método con `login_required` + `permiso_requerido('x.y')`:

```python
bp.route('/ruta-protegida')(
    login_required(
        permiso_requerido('modulo.accion')(controller.metodo)
    )
)
```

### 4.7 Helpers — `app/helpers/`

**`decorators.py`**:

```python
def permiso_requerido(codigo):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if not current_user.tiene_permiso(codigo):
                flash('No tienes permiso para acceder a esta página', 'danger')
                return redirect(url_for('dashboard.panel'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

**`bitacora_helper.py`**: Helper contextual que extrae automáticamente `current_user.id`, `request.path`, `request.remote_addr` para no repetirlos en cada controller.

### 4.8 Traits — `app/traits/validaciones.py`

Equivalente a un `trait` en PHP. Mixin que agrega métodos de validación reutilizables a cualquier clase:

```python
class ValidacionesMixin:
    errores: list = []

    def validar_obligatorios(self, campos, datos) -> bool: ...
    def validar_longitud(self, texto, min_len, max_len, campo) -> bool: ...
    def validar_fecha(self, fecha_str, campo='fecha') -> bool: ...
    def sanitizar_texto(self, texto) -> str: ...
    def get_errores(self) -> list: ...
    def limpiar_errores(self): ...
    def tiene_errores(self) -> bool: ...
```

Uso: `class MiServicio(ValidacionesMixin):`

---

## 5. Sistema de Roles y Permisos

### 5.1 Modelos

| Entidad | Tabla | Propósito |
|---|---|---|
| `Rol` | `roles` | Roles del sistema (Superadmin, Administrador, Usuario) |
| `Permiso` | `permisos` | Catálogo de 25 permisos individuales |
| `RolPermiso` | `rol_permiso` | Permisos base asignados a cada rol |
| `UsuarioPermiso` | `usuario_permiso` | Permisos extra asignados directamente a un usuario |

### 5.2 Catálogo de Permisos (25)

| Módulo | Permisos |
|---|---|
| Dashboard | `dashboard.view` |
| Guión | `guion.view`, `create`, `.edit`, `.delete`, `.preview`, `.publish` |
| En Vivo | `envivo.view`, `envivo.control` |
| Mantenimiento | `mantenimiento.view`, `.create`, `.edit`, `.delete` |
| Premios | `premio.view`, `.create`, `.edit`, `.delete`, `.entregar` |
| Usuarios | `usuario.view`, `.create`, `.edit`, `.delete`, `.perfil` |
| Roles | `rol.view`, `.create`, `.edit` |

### 5.3 Seed Automático

En `app/__init__.py` al arrancar la app, si no existen roles:

```python
with app.app_context():
    from app.repositories.rol_repository import RolRepository
    repo = RolRepository()
    if not repo.consultar():
        from app.services.rol_service import RolService
        RolService().seed_permisos_iniciales()
```

El seed es **idempotente**: si ya hay datos, no hace nada.

### 5.4 Verificación de Permisos

**En la entidad Usuario** (`tiene_permiso`):

```python
def tiene_permiso(self, codigo):
    if self.is_superadmin():
        return True                          # ← Superadmin tiene TODO
    if self._permisos_cache is None:
        from app.repositories.rol_repository import RolRepository
        # Carga permisos del rol + permisos individuales en UNA consulta UNION
        self._permisos_cache = RolRepository().obtener_permisos_usuario(
            self.id, self.rol
        )
    return codigo in self._permisos_cache    # ← búsqueda en set (O(1))
```

**Claves de diseño**:
- **Cache**: Los permisos se cargan UNA vez por request y se cachean en `_permisos_cache`. La segunda llamada a `tiene_permiso()` no hace otra consulta.
- **Superadmin bypass**: `is_superadmin()` retorna True, saltando toda la verificación.
- **UNION SQL**: La consulta en el repositorio usa `UNION` para combinar permisos del rol + permisos individuales en una sola llamada a la BD.

---

## 6. Módulo Auth (Login/Logout)

### 6.1 Login (`/auth/login`)

```
GET /auth/login → renderiza login.html con LoginForm
    │
POST /auth/login (submit)
    ├── LoginForm.validate_on_submit() (Flask-WTF + CSRF)
    ├── UsuarioRepository.obtener_por_email(email)
    ├── usuario.check_password(password)
    ├── Verifica usuario.activo
    ├── login_user(usuario, remember)
    ├── UsuarioRepository.actualizar_ultimo_acceso(id)
    ├── [Bitácora] iniciar_sesion() → guarda sesion_id en flask.session
    └── redirect(url_for('dashboard.panel'))
```

**Animación JS**: El formulario tiene un `onsubmit` que previene el envío inmediato, muestra animación de pelotas por ~2.5s, y luego llama `HTMLFormElement.prototype.submit.call(form)`.

### 6.2 Logout (`/auth/logout`)

```
POST /auth/logout
    ├── Recupera sesion_id de flask.session
    ├── [Bitácora] finalizar_sesion(sesion_id)
    ├── [Bitácora] registrar_actividad('logout', 'auth', ...)
    ├── logout_user() (Flask-Login)
    └── redirect(url_for('auth.login'))
```

### 6.3 user_loader (Flask-Login)

En `app/__init__.py`:

```python
@login_manager.user_loader
def load_user(user_id):
    from app.repositories.usuario_repository import UsuarioRepository
    return UsuarioRepository().obtener_por_id(int(user_id))
```

**Importante**: `user_loader` está importado dentro de la función para evitar import cíclico.

---

## 7. Módulo Bitácora (Auditoría)

### 7.1 Modelos

```
sesiones_usuario          actividad_usuario          cambios_por_modulo
┌──────────────┐          ┌──────────────────┐       ┌───────────────────┐
│ id (PK)      │──┐      │ id (PK)          │──┐    │ id (PK)           │
│ usuario_id   │  │     │ sesion_id (FK) ──┘  │    │ actividad_id (FK) │
│ inicio_sesion│  ├──────│ usuario_id (FK)     │    │ tabla_afectada    │
│ fin_sesion   │  │     │ tipo_accion        │    │ registro_id        │
│ ip_address   │  │     │ modulo             │    │ campo              │
│ user_agent   │  │     │ accion             │    │ valor_anterior     │
│ duracion_seg │  │     │ detalle (JSON)     │    │ valor_nuevo        │
└──────────────┘  │     │ pagina             │    └───────────────────┘
                  │     │ created_at         │
                  │     └──────────────────┘
                  │
                  │     errores_aplicacion
                  │     ┌──────────────────┐
                  └─────│ usuario_id (FK)   │
                        │ tipo_error        │
                        │ mensaje           │
                        │ traceback         │
                        │ pagina            │
                        └──────────────────┘
```

### 7.2 Integración

Desde cualquier controller:

```python
from app.helpers.bitacora_helper import registrar_actividad

# Después de una operación exitosa:
registrar_actividad('create', 'mi_modulo', 'Crear X',
                    f'X "{nombre}" creado')
```

El helper extrae automáticamente:
- `current_user.id`
- `request.path`
- `request.remote_addr`

### 7.3 Dashboard de Bitácora

- **`GET /bitacora/`**: Cards resumen + tabla de actividad reciente + errores.
- **`GET /bitacora/usuario/<id>`**: Reporte detallado con filtros (fecha, módulo, tipo), tiempo estimado por módulo, sesiones, cambios (antes→después), errores.

---

## 8. Módulo Dashboard + SocketIO

### 8.1 Dashboard Principal (`/dashboard`)

Muestra:
- **Guión en vivo**: Si hay un guión con estado `en_vivo`, muestra nombre, fecha, progreso (completados/total).
- **Usuarios en línea**: Contador de sockets conectados vía dict global `usuarios_conectados`.
- **Warning Song**: Elementos en curso o pendientes del guión activo.

### 8.2 SocketIO — Usuarios Conectados

En `app/__init__.py`:

```python
usuarios_conectados = {}  # dict global: sid → {user_id, nombre, pagina, en_vivo_id}

@socketio.on('registrar_usuario')
def handle_registrar_usuario(data):
    sid = request.sid
    usuarios_conectados[sid] = {
        'user_id': data.get('user_id'),
        'nombre': data.get('nombre'),
        'pagina': data.get('pagina', '/'),
        'en_vivo_id': data.get('en_vivo_id')
    }
    _emit_usuarios_actualizados()  # Broadcast a TODOS los clientes

@socketio.on('cambio_pagina')
def handle_cambio_pagina(data):
    """Actualiza la página actual del usuario en el tracking."""
    sid = request.sid
    if sid in usuarios_conectados:
        usuarios_conectados[sid]['pagina'] = data.get('pagina', '/')
        usuarios_conectados[sid]['en_vivo_id'] = data.get('en_vivo_id')
        _emit_usuarios_actualizados()

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    usuarios_conectados.pop(sid, None)
    _emit_usuarios_actualizados()
```

**Flujo completo**:
1. Cliente abre la página → evento `connect` (automático)
2. Cliente JS emite `registrar_usuario` con `{user_id, nombre}`
3. Servidor guarda en `usuarios_conectados` y hace broadcast
4. Todos los clientes reciben `usuarios_actualizados` con count + lista
5. Al cerrar pestaña → `disconnect` → se remueve del dict

### 8.3 SocketIO — Sincronización de Guión en Vivo

Cuando un controlador modifica estados en el guión en vivo:

```python
# en_vivo_controller.py
def sincronizar(self, guion_id):
    data = request.get_json()
    estados = data.get('estados', [])
    self.service.sincronizar_estados(guion_id, estados)
    socketio.emit('actualizar_estados', {
        'guion_id': guion_id,
        'estados': estados
    })  # ← Broadcast a TODOS los que ven el guión
    return jsonify({'success': True})
```

**CSRF Exempt**: El blueprint `en_vivo` está exento de CSRF porque SocketIO usa su propio mecanismo de seguridad:

```python
csrf.exempt(en_vivo_routes.bp)
```

---

## 9. Módulo Guión + En Vivo

### 9.1 Modelos

```python
Guion:          id, nombre, estado (borrador/publicado/en_vivo/finalizado),
                creado_en, modificado_en
GuionFecha:     id, guion_id (FK), fecha
ElementoGuion:  id, guion_id (FK), fecha_id, tipo (pregame/game),
                hora (pregame), inning + medio_inning (game),
                contenido, duracion_estimada, encargado, orden, estado
```

### 9.2 Flujo Completo

```
1. Crear guión         → POST /guiones/crear (nombre + fechas)
2. Agregar elementos   → POST /guiones/agregar-elemento/<id>
   ├── Pre-Game: hora + contenido + encargado
   └── Game: inning + medio_inning + contenido + encargado
3. Previsualizar       → GET /guiones/previsualizar/<id>
4. Publicar            → POST /guiones/publicar/<id> (estado → 'publicado')
5. Iniciar en vivo     → GET /en-vivo/iniciar/<id> (estado → 'en_vivo')
6. Controlar en vivo   → GET /en-vivo/<id> (pantalla de control)
7. Finalizar           → GET /en-vivo/finalizar/<id> (estado → 'finalizado')
```

### 9.3 Validaciones de Elementos

```python
# guion_service.py
def agregar_elemento(self, guion_id, data):
    # 1. Pre-Game requiere hora
    # 2. Game requiere inning + medio_inning
    # 3. Hora no puede estar ocupada por otro pregame
    # 4. Inning no puede estar ocupado por otro game
    # 5. Auto-asigna orden (último_orden + 1)
```

### 9.4 Pantalla en Vivo

- **`/en-vivo/<guion_id>`**: Pantalla completa con todos los elementos.
- **Doble clic**: Marca elemento como completado (gris tachado).
- **Botón ↩**: Retrocede un estado.
- **SocketIO**: Sincroniza cambios entre todos los clientes conectados al mismo guión.
- Elementos PREGAME ordenados por hora; GAME ordenados por inning.

---

## 10. Módulo Mantenimiento

### 10.1 Ciclo de Estados

```
disponible → [ingresar] → en_mantenimiento (en_espera)
en_espera → [reparar] → en_reparacion
en_reparacion → [reparar] → reparado
reparado → [finalizar] → finalizado
cualquier estado → [dar_baja] → baja
```

Cada transición:
1. Actualiza el estado en `mantenimientos` y (si aplica) en `recursos`
2. Crea un registro en `historial_mantenimiento`
3. Registra en bitácora vía `registrar_actividad()`

### 10.2 Relaciones Cross-DB

`Mantenimiento.usuario_id` es INTEGER sin FK real porque apunta a `no_funcional.usuarios`. El repositorio carga el nombre del usuario mediante el método `_cargar_relaciones()` que usa `UsuarioRepository`.

---

## 11. Módulo Premios

### 11.1 Modelos

```python
Premio:         id, nombre, descripcion, id_patrocinador (FK), estado,
                estatus (borrado lógico), fecha_creacion, hora_creacion,
                foto, fecha_entrega, entregado_por (INTEGER)
Patrocinador:   id_patrocinador, nombre_empresa
```

### 11.2 Acciones (todo via POST a `/premios/`)

| action | Qué hace |
|---|---|
| `crear` | Crea nuevo premio con foto opcional |
| `editar` | Edita nombre, patrocinador, descripción, foto |
| `entregar` | Cambia estado a `entregado` con timestamp |
| `crear_y_entregar` | Entrega premio existente con patrocinador opcional |

### 11.3 Borrado Lógico

`estatus = TRUE` marca el premio como eliminado. Todas las consultas activas incluyen `WHERE estatus = FALSE`.

---

## 12. Módulo Usuarios

### 12.1 Entidad Usuario

```python
class Usuario:
    def __init__(self, id=None, nombre=None, email=None, ...):
        ...
        self._permisos_cache = None  # ← Cache de permisos

    # Flask-Login interface:
    @property
    def is_authenticated(self): return True
    @property
    def is_active(self): return self.activo
    def get_id(self): return str(self.id)

    # Auth:
    def set_password(self, password): ...
    def check_password(self, password): ...

    # Permisos:
    def is_superadmin(self): return self.rol == 'Superadmin'
    def is_admin(self): return self.rol in ('Administrador', 'Superadmin')
    def tiene_permiso(self, codigo): ...  # ← usa RolRepository + cache
```

### 12.2 Roles del Sistema

| Rol | Acceso |
|---|---|
| `Superadmin` | Todos los permisos automáticamente |
| `Administrador` | Permisos según rol (sin `rol.*`) |
| `Usuario` | Solo lectura: dashboard, guion, en_vivo, perfil |

---

## 13. Cómo Crear un Módulo desde Cero

Guía paso a paso para agregar un nuevo módulo (ej: "Categorías") siguiendo todos los patrones del sistema.

### Paso 1: Crear la Entidad (POPO)

Archivo: `app/models/categoria.py`

```python
class Categoria:
    def __init__(self, id=None, nombre=None, descripcion='', activo=True,
                 creado_en=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.activo = bool(activo) if activo is not None else True
        self.creado_en = creado_en
        self.propiedad_cargada = None  # ← Default ANTES de kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)  # ← kwargs al FINAL
```

### Paso 2: Crear el Repositorio

Archivo: `app/repositories/categoria_repository.py`

```python
from app.repositories.base_repository import BaseRepository
from app.models.categoria import Categoria

class CategoriaRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')  # ← o 'no_funcional' según corresponda

    def consultar(self, **filtros):
        sql = "SELECT * FROM categorias WHERE 1=1"
        params = []
        if filtros.get('activo') is not None:
            sql += " AND activo = %s"
            params.append(1 if filtros['activo'] else 0)
        sql += " ORDER BY nombre ASC"
        rows = self.fetch_all(sql, params)
        return [Categoria(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM categorias WHERE id = %s", (id,))
        return Categoria(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO categorias (nombre, descripcion, activo, creado_en) VALUES (%s, %s, %s, NOW())",
            (datos['nombre'], datos.get('descripcion', ''), 1)
        )
        return self.obtener_por_id(id)

    def modificar(self, id, datos):
        sets = []
        params = []
        for campo in ['nombre', 'descripcion', 'activo']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id)
            self.execute(f"UPDATE categorias SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id)

    def eliminar(self, id):
        self.execute("DELETE FROM categorias WHERE id = %s", (id,))
```

### Paso 3: Crear el Servicio

Archivo: `app/services/categoria_service.py`

```python
from app.repositories.categoria_repository import CategoriaRepository
from app.traits.validaciones import ValidacionesMixin

class CategoriaService(ValidacionesMixin):
    def __init__(self):
        self.repo = CategoriaRepository()

    def obtener_todas(self):
        return self.repo.consultar(activo=True)

    def crear(self, nombre, descripcion=''):
        self.limpiar_errores()
        self.validar_obligatorios(['nombre'], {'nombre': nombre})
        self.validar_longitud(nombre, 2, 100, 'nombre')
        if self.tiene_errores():
            return None
        return self.repo.registrar({
            'nombre': nombre,
            'descripcion': descripcion,
        })

    def editar(self, id, nombre, descripcion=''):
        self.limpiar_errores()
        self.validar_obligatorios(['nombre'], {'nombre': nombre})
        if self.tiene_errores():
            return None
        return self.repo.modificar(id, {
            'nombre': nombre,
            'descripcion': descripcion,
        })

    def eliminar(self, id):
        return self.repo.eliminar(id)
```

### Paso 4: Crear el Controlador

Archivo: `app/controllers/categoria_controller.py`

```python
from flask import render_template, request, redirect, url_for, flash
from app.services.categoria_service import CategoriaService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad

class CategoriaController:
    def __init__(self):
        self.service = CategoriaService()

    def listar(self):
        categorias = self.service.obtener_todas()
        return render_template('categoria/lista.html', categorias=categorias)

    def crear(self):
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion', '')
            resultado = self.service.crear(nombre, descripcion)
            if resultado:
                registrar_actividad('create', 'categorias', 'Crear categoría',
                                    f'Categoría "{nombre}" creada')
                flash(f'Categoría "{nombre}" creada', 'success')
                return redirect(url_for('categoria.listar'))
            for error in self.service.get_errores():
                flash(error, 'danger')
        return render_template('categoria/crear.html')
```

### Paso 5: Crear las Rutas

Archivo: `app/routes/categoria_routes.py`

```python
from flask import Blueprint
from app.controllers.categoria_controller import CategoriaController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('categoria', __name__, url_prefix='/categorias')
controller = CategoriaController()

bp.route('/')(
    login_required(permiso_requerido('categoria.view'))(controller.listar)
)
bp.route('/crear', methods=['GET', 'POST'])(
    login_required(permiso_requerido('categoria.create'))(controller.crear)
)
```

### Paso 6: Registrar el Blueprint en `app/__init__.py`

```python
# Al final de create_app(), junto a los otros:
from app.routes import categoria_routes
app.register_blueprint(categoria_routes.bp)
```

### Paso 7: Agregar Permisos al Seed

En `app/services/rol_service.py`, agregar al array `PERMISOS_CATALOGO`:

```python
{'codigo': 'categoria.view', 'nombre': 'Ver categorías', 'modulo': 'Categorías'},
{'codigo': 'categoria.create', 'nombre': 'Crear categorías', 'modulo': 'Categorías'},
```

### Paso 8: Integrar Bitácora

Ya está en el paso 4 (el controller llama `registrar_actividad`). Para cambios detallados (antes→después), usar:

```python
from app.helpers.bitacora_helper import registrar_cambio
registrar_cambio('categorias', 'nombre', valor_anterior='Viejo', valor_nuevo='Nuevo', registro_id=id)
```

### Resumen de archivos a crear para un módulo

| # | Archivo | Contenido |
|---|---|---|
| 1 | `app/models/categoria.py` | Entidad POPO |
| 2 | `app/repositories/categoria_repository.py` | SQL nativo |
| 3 | `app/services/categoria_service.py` | Lógica de negocio |
| 4 | `app/controllers/categoria_controller.py` | Clase con DI |
| 5 | `app/routes/categoria_routes.py` | Blueprint |
| 6 | `app/templates/categoria/` | Carpeta de vistas |
| 7 | `app/forms/categoria_form.py` | Formulario (opcional) |
| 8 | Modificar `app/__init__.py` | Registrar blueprint |
| 9 | Modificar `app/services/rol_service.py` | Agregar permisos al seed |

---

## 14. Principios SOLID Aplicados

### S — Single Responsibility (Responsabilidad Única)

| Capa | Responsabilidad | No hace |
|---|---|---|
| Entity | Transportar datos | SQL, lógica, HTTP |
| Repository | Ejecutar SQL | Lógica de negocio, HTTP |
| Service | Lógica de negocio | SQL, HTTP |
| Controller | Manejar HTTP | SQL, lógica compleja |
| Route | Mapear URL → método | Todo lo demás |

### O — Open/Closed (Abierto/Cerrado)

- **Abierto a extensión**: Para agregar una nueva consulta, creas un método en el repositorio (no modificas la entidad).
- **Cerrado a modificación**: La entidad no cambia cuando agregas columnas (kwargs lo absorbe).

### L — Liskov Substitution

```python
class BaseRepository:  # ← Contrato
    def fetch_all(...): ...
    def fetch_one(...): ...
    def execute(...): ...

class UsuarioRepository(BaseRepository):  # ← Sustituye a BaseRepository
    def obtener_por_email(self, email): ...
    # + todos los métodos de BaseRepository funcionan igual
```

### I — Interface Segregation (Segregación de Interfaces)

Cada repositorio expone **solo los métodos que necesita**:

- `UsuarioRepository`: `obtener_por_email()`, `actualizar_ultimo_acceso()`
- `GuionRepository`: `obtener_fechas()`, `contar(estado='borrador')`
- `EnVivoRepository`: `iniciar_en_vivo()`, `finalizar_en_vivo()`

Ningún repositorio está forzado a implementar métodos que no usa.

### D — Dependency Inversion (Inversión de Dependencias)

```python
# ❌ Incorrecto: Controller crea su propia conexión
class Controller:
    def metodo(self):
        conn = pymysql.connect(...)  # ← Acoplamiento rígido

# ✅ Correcto: Controller depende de una abstracción (el repositorio)
class Controller:
    def __init__(self):
        self.repo = UsuarioRepository()  # ← Fácil de cambiar/mockear
```

---

## 15. Patrones de Diseño Usados

| Patrón | Dónde | Cómo |
|---|---|---|
| **Repository** | `app/repositories/` | Separa la lógica de acceso a datos del resto de la app |
| **Data Mapper** | `models/` + `repositories/` | Las entidades ignoran la BD; los repositorios mapean filas a objetos |
| **Front Controller** | Flask (`app/__init__.py`) | Punto único de entrada que centraliza peticiones |
| **Dependency Injection** | `controllers/` | Los controllers reciben repositorios/servicios en `__init__` |
| **Mixin / Trait** | `traits/validaciones.py` | Agrega métodos de validación a cualquier clase sin herencia múltiple |
| **Singleton por Request** | `database/connection.py` | `DatabaseManager.get_connection()` retorna la misma conexión dentro de una request |
| **Strategy** | `services/` | Diferentes servicios encapsulan diferentes algoritmos de negocio |
| **Lazy Loading** | `models/usuario.py` | `_permisos_cache` se carga solo cuando se necesita |

---

## 16. Apéndice

### 16.1 Dependencias (requirements.txt)

```
Flask==3.1.3
Flask-Login==0.6.3
Flask-SocketIO==5.6.1
Flask-WTF==1.3.0
PyMySQL==1.2.0
Werkzeug==3.1.8
WTForms==3.2.2
python-socketio==5.16.1
```

### 16.2 Scripts

| Script | Propósito |
|---|---|
| `run.py` | Iniciar servidor: `python3 run.py` |
| `crear_admin.py` | Crear Superadmin inicial |
| `estadio_db.sql` | CREATE TABLE de la base funcional |
| `no_funcional.sql` | CREATE TABLE de la base no funcional |

### 16.3 Restaurar desde Cero

```bash
mysql -u root -p < estadio_db.sql
mysql -u root -p < no_funcional.sql
python3 crear_admin.py
python3 run.py
```

### 16.4 Preguntas Frecuentes

**¿Cómo creo un Superadmin?**
```bash
python3 crear_admin.py
```
O manualmente insertando en `no_funcional.usuarios` con rol `Superadmin`.

**¿Dónde van los templates?**
En `app/templates/<modulo>/`. Sin cambios estructurales — Jinja2 funciona con objetos que tengan los atributos correctos.

**¿Cómo agrego un nuevo permiso?**
1. Agregar al array `PERMISOS_CATALOGO` en `app/services/rol_service.py`
2. Agregar al array `PERMISOS_POR_ROL` si un rol base debe tenerlo
3. Al reiniciar, el seed automático lo crea (es idempotente)

**¿Cómo conecto a la BD desde un script externo?**
```python
from app.database.connection import DatabaseManager
conn = DatabaseManager.get_connection('estadio_db')
with conn.cursor() as cur:
    cur.execute("SELECT * FROM ...")
    rows = cur.fetchall()
```

**¿Por qué no usamos SQLAlchemy?**
Porque queremos control total sobre el SQL que se ejecuta, sin magia de ORM, siguiendo el estilo PDO de PHP que es más explícito y predecible para consultas complejas.

**¿Las entidades soportan serialización JSON?**
Sí, cualquier entidad se puede pasar a `jsonify()` porque sus atributos son accesibles como `obj.atributo`. Para estructuras anidadas, usar `to_dict()`.

### 16.5 Checklist para Nuevo Desarrollador

- [ ] Entender el flujo de una petición (punto 2.3)
- [ ] Conocer DatabaseManager (punto 3.2)
- [ ] Leer el patrón de entidades POPO (punto 4.1)
- [ ] Entender BaseRepository (punto 4.2)
- [ ] Revisar el sistema de roles/permisos (punto 5)
- [ ] Leer la guía completa de crear módulo (punto 13)
- [ ] Revisar el blueprint de rutas más simple (ej: `auth_routes.py`)
- [ ] Probar creando un módulo pequeño siguiendo el paso a paso
