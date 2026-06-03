# migrar_a_dual_db.py
# Migra datos de estadio_db -> no_funcional y adapta estadio_db
# Ejecutar: python3 migrar_a_dual_db.py

import pymysql
from datetime import datetime

MYSQL = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}


def get_conn(database=None):
    conn = pymysql.connect(
        host=MYSQL['host'], port=MYSQL['port'],
        user=MYSQL['user'], password=MYSQL['password'],
        charset=MYSQL['charset'], autocommit=False,
        database=database
    )
    return conn


def main():
    print("=" * 60)
    print("Migración: estadio_db → estadio_db + no_funcional")
    print("=" * 60)

    conn_estadio = get_conn('estadio_db')

    # ─── 1. RESPALDAR DATOS DE TABLAS QUE SE MUEVEN ───
    print("\n📦 Respaldo datos de tablas que se moverán...")

    cur = conn_estadio.cursor(pymysql.cursors.DictCursor)

    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    print(f"  usuarios: {len(usuarios)} filas")

    cur.execute("SELECT * FROM roles")
    roles = cur.fetchall()
    print(f"  roles: {len(roles)} filas")

    cur.execute("SELECT * FROM permisos")
    permisos = cur.fetchall()
    print(f"  permisos: {len(permisos)} filas")

    cur.execute("SELECT * FROM rol_permiso")
    rol_permiso = cur.fetchall()
    print(f"  rol_permiso: {len(rol_permiso)} filas")

    cur.execute("SELECT * FROM usuario_permiso")
    usuario_permiso = cur.fetchall()
    print(f"  usuario_permiso: {len(usuario_permiso)} filas")

    cur.close()

    # ─── 2. CREAR DB no_funcional ───
    print("\n🏗️  Creando base de datos no_funcional...")
    conn_root = get_conn()
    with conn_root.cursor() as c:
        c.execute("CREATE DATABASE IF NOT EXISTS `no_funcional` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn_root.commit()
    conn_root.close()
    print("  ✅ no_funcional creada")

    # ─── 3. CREAR TABLAS EN no_funcional ───
    print("\n📋 Creando tablas en no_funcional...")
    conn_nf = get_conn('no_funcional')

    TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS `usuarios` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nombre` varchar(100) NOT NULL,
      `email` varchar(100) NOT NULL,
      `password_hash` varchar(200) NOT NULL,
      `cedula` varchar(20) NOT NULL,
      `rol` varchar(20) DEFAULT 'Usuario',
      `departamento` varchar(50) DEFAULT 'Medios',
      `telefono` varchar(20) DEFAULT NULL,
      `activo` tinyint(1) DEFAULT 1,
      `fecha_registro` datetime DEFAULT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `email` (`email`),
      UNIQUE KEY `cedula` (`cedula`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `roles` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nombre` varchar(50) NOT NULL,
      `descripcion` text,
      PRIMARY KEY (`id`),
      UNIQUE KEY `nombre` (`nombre`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `permisos` (
      `id` int NOT NULL AUTO_INCREMENT,
      `nombre` varchar(100) NOT NULL,
      `codigo` varchar(100) NOT NULL,
      `modulo` varchar(50) NOT NULL,
      `descripcion` text,
      PRIMARY KEY (`id`),
      UNIQUE KEY `codigo` (`codigo`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `rol_permiso` (
      `id` int NOT NULL AUTO_INCREMENT,
      `rol_id` int NOT NULL,
      `permiso_id` int NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `rol_permiso_unique` (`rol_id`, `permiso_id`),
      CONSTRAINT `rp_fk_rol` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`),
      CONSTRAINT `rp_fk_permiso` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `usuario_permiso` (
      `id` int NOT NULL AUTO_INCREMENT,
      `usuario_id` int NOT NULL,
      `permiso_id` int NOT NULL,
      `fecha_asignacion` datetime DEFAULT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `usuario_permiso_unique` (`usuario_id`, `permiso_id`),
      CONSTRAINT `up_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
      CONSTRAINT `up_fk_permiso` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `sesiones_usuario` (
      `id` int NOT NULL AUTO_INCREMENT,
      `usuario_id` int NOT NULL,
      `inicio_sesion` datetime DEFAULT NULL,
      `fin_sesion` datetime DEFAULT NULL,
      `ip_address` varchar(45) DEFAULT NULL,
      `user_agent` varchar(500) DEFAULT NULL,
      `duracion_segundos` int DEFAULT NULL,
      PRIMARY KEY (`id`),
      CONSTRAINT `su_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `actividad_usuario` (
      `id` int NOT NULL AUTO_INCREMENT,
      `sesion_id` int DEFAULT NULL,
      `usuario_id` int NOT NULL,
      `tipo_accion` varchar(30) NOT NULL,
      `modulo` varchar(50) NOT NULL,
      `accion` text,
      `detalle` json DEFAULT NULL,
      `pagina` varchar(200) DEFAULT NULL,
      `ip_address` varchar(45) DEFAULT NULL,
      `created_at` datetime DEFAULT NULL,
      PRIMARY KEY (`id`),
      CONSTRAINT `au_fk_sesion` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones_usuario` (`id`),
      CONSTRAINT `au_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `cambios_por_modulo` (
      `id` int NOT NULL AUTO_INCREMENT,
      `actividad_id` int NOT NULL,
      `tabla_afectada` varchar(50) NOT NULL,
      `registro_id` int DEFAULT NULL,
      `campo` varchar(100) NOT NULL,
      `valor_anterior` text,
      `valor_nuevo` text,
      `created_at` datetime DEFAULT NULL,
      PRIMARY KEY (`id`),
      CONSTRAINT `cm_fk_actividad` FOREIGN KEY (`actividad_id`) REFERENCES `actividad_usuario` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

    CREATE TABLE IF NOT EXISTS `errores_aplicacion` (
      `id` int NOT NULL AUTO_INCREMENT,
      `usuario_id` int DEFAULT NULL,
      `tipo_error` varchar(50) DEFAULT NULL,
      `mensaje` text,
      `traceback` text,
      `pagina` varchar(200) DEFAULT NULL,
      `ip_address` varchar(45) DEFAULT NULL,
      `created_at` datetime DEFAULT NULL,
      PRIMARY KEY (`id`),
      CONSTRAINT `ea_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    # Drop existing tables first to avoid conflicts
    for statement in TABLES_SQL.split(';'):
        s = statement.strip()
        if s:
            try:
                with conn_nf.cursor() as c:
                    c.execute(s)
                conn_nf.commit()
            except pymysql.err.OperationalError as e:
                print(f"  ⚠️  {e}")
                conn_nf.rollback()
    print("  ✅ Tablas creadas en no_funcional")

    # ─── 4. INSERTAR DATOS EN no_funcional ───
    print("\n📤 Insertando datos en no_funcional...")

    nf_cur = conn_nf.cursor()

    # Insert usuarios (usar IDs originales)
    for u in usuarios:
        nf_cur.execute(
            "INSERT INTO `usuarios` (id, nombre, email, password_hash, cedula, rol, departamento, telefono, activo, fecha_registro) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (u['id'], u['nombre'], u['email'], u['password_hash'], u['cedula'],
             u['rol'], u['departamento'], u['telefono'], u['activo'], u['fecha_registro'])
        )
    conn_nf.commit()
    print(f"  ✅ usuarios: {len(usuarios)} insertados")

    # Insert roles (usar IDs originales)
    for r in roles:
        nf_cur.execute(
            "INSERT INTO `roles` (id, nombre, descripcion) VALUES (%s, %s, %s)",
            (r['id'], r['nombre'], r['descripcion'])
        )
    conn_nf.commit()
    print(f"  ✅ roles: {len(roles)} insertados")

    # Insert permisos (usar IDs originales)
    for p in permisos:
        nf_cur.execute(
            "INSERT INTO `permisos` (id, nombre, codigo, modulo, descripcion) VALUES (%s, %s, %s, %s, %s)",
            (p['id'], p['nombre'], p['codigo'], p['modulo'], p['descripcion'])
        )
    conn_nf.commit()
    print(f"  ✅ permisos: {len(permisos)} insertados")

    # Insert rol_permiso (usar IDs originales)
    for rp in rol_permiso:
        nf_cur.execute(
            "INSERT INTO `rol_permiso` (id, rol_id, permiso_id) VALUES (%s, %s, %s)",
            (rp['id'], rp['rol_id'], rp['permiso_id'])
        )
    conn_nf.commit()
    print(f"  ✅ rol_permiso: {len(rol_permiso)} insertados")

    # Insert usuario_permiso
    for up in usuario_permiso:
        nf_cur.execute(
            "INSERT INTO `usuario_permiso` (id, usuario_id, permiso_id, fecha_asignacion) VALUES (%s, %s, %s, %s)",
            (up['id'], up['usuario_id'], up['permiso_id'], up.get('fecha_asignacion'))
        )
    conn_nf.commit()
    print(f"  ✅ usuario_permiso: {len(usuario_permiso)} insertados")

    nf_cur.close()
    conn_nf.close()

    # ─── 5. ELIMINAR TABLAS MOVIDAS DE estadio_db ───
    print("\n🗑️  Eliminando tablas movidas de estadio_db...")
    with conn_estadio.cursor() as c:
        c.execute("SET FOREIGN_KEY_CHECKS = 0")
        c.execute("DROP TABLE IF EXISTS `usuario_permiso`")
        c.execute("DROP TABLE IF EXISTS `rol_permiso`")
        c.execute("DROP TABLE IF EXISTS `permisos`")
        c.execute("DROP TABLE IF EXISTS `roles`")
        c.execute("DROP TABLE IF EXISTS `usuarios`")
        c.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn_estadio.commit()
    print("  ✅ Tablas eliminadas: usuarios, roles, permisos, rol_permiso, usuario_permiso")

    # ─── 6. ELIMINAR COLUMNA fecha_hora_creacion DE premios si existe ───
    print("\n🔧 Limpiando esquema de premios...")
    try:
        with conn_estadio.cursor() as c:
            c.execute("ALTER TABLE `premios` DROP COLUMN IF EXISTS `fecha_hora_creacion`")
        conn_estadio.commit()
        print("  ✅ Columna fecha_hora_creacion eliminada de premios")
    except pymysql.err.OperationalError as e:
        print(f"  ℹ️  {e}")
        conn_estadio.rollback()

    conn_estadio.close()

    print("\n" + "=" * 60)
    print("✅ Migración completada exitosamente!")
    print("   - estadio_db: solo tablas funcionales")
    print("   - no_funcional: usuarios, roles, permisos, bitácora")
    print("=" * 60)


if __name__ == '__main__':
    main()
