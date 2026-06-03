# migrar_a_mysql.py
# 1. Inicia XAMPP MySQL
# 2. Crea la DB: mysql -u root -e "CREATE DATABASE IF NOT EXISTS estadio_db"
# 3. Ejecuta: python3 migrar_a_mysql.py

import sqlite3
import pymysql
from datetime import date, time, datetime

# Configuración MySQL (XAMPP default)
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'estadio_db',
    'charset': 'utf8mb4'
}

SQLITE_PATHS = ['instance/usuarios.db', 'instance/estadio.db', 'estadio.db', 'usuarios.db']


def get_active_sqlite():
    """Encuentra la DB de SQLite con más datos"""
    best = None
    best_count = -1
    for path in SQLITE_PATHS:
        try:
            conn = sqlite3.connect(path)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = c.fetchall()
            total = 0
            for t in tables:
                c.execute(f"SELECT COUNT(*) FROM {t[0]}")
                total += c.fetchone()[0]
            conn.close()
            if total > best_count:
                best_count = total
                best = path
        except:
            pass
    return best


def get_sqlite_conn(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def get_mysql_conn():
    conn = pymysql.connect(
        host=MYSQL_CONFIG['host'],
        port=MYSQL_CONFIG['port'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        charset=MYSQL_CONFIG['charset'],
        autocommit=False
    )
    return conn


def create_database():
    conn = get_mysql_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        print("✅ Base de datos 'estadio_db' creada/verificada")
    finally:
        conn.close()


def create_tables_in_mysql():
    """Usa SQLAlchemy para crear todas las tablas en MySQL"""
    from app import create_app, db
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas en MySQL")


def safe_value(val):
    if val is None:
        return None
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, (date, time, datetime)):
        return str(val)
    return val


def migrate_table(table_name, columns, rows):
    if not rows:
        print(f"  ℹ️  {table_name}: sin datos")
        return

    conn = get_mysql_conn()
    conn.select_db(MYSQL_CONFIG['database'])
    try:
        with conn.cursor() as cur:
            placeholders = ', '.join(['%s'] * len(columns))
            cols = ', '.join([f'`{c}`' for c in columns])
            sql = f"INSERT IGNORE INTO `{table_name}` ({cols}) VALUES ({placeholders})"

            inserted = 0
            for row in rows:
                values = [safe_value(row[c]) for c in columns]
                try:
                    cur.execute(sql, values)
                    inserted += 1
                except pymysql.err.IntegrityError as e:
                    print(f"  ⚠️  {table_name}: fila duplicada - {e}")

            conn.commit()
            print(f"  ✅ {table_name}: {inserted}/{len(rows)} filas migradas")
    finally:
        conn.close()


def main():
    print("=" * 50)
    print("🚀 Migración de SQLite a MySQL (XAMPP)")
    print("=" * 50)

    # 1. Encontrar SQLite con datos
    sqlite_path = get_active_sqlite()
    if not sqlite_path:
        print("❌ No se encontró ninguna base SQLite")
        return
    print(f"\n📁 Usando: {sqlite_path}")

    # 2. Crear DB en MySQL
    print("\n📦 Creando base de datos en MySQL...")
    create_database()

    # 3. Leer datos de SQLite
    print(f"\n📖 Leyendo datos de {sqlite_path}...")
    sqlite_conn = get_sqlite_conn(sqlite_path)
    sqlite_cur = sqlite_conn.cursor()
    sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in sqlite_cur.fetchall()]
    print(f"  Tablas encontradas: {', '.join(tables)}")

    all_data = {}
    for table in tables:
        sqlite_cur.execute(f"SELECT * FROM {table}")
        rows = sqlite_cur.fetchall()
        sqlite_cur.execute(f"PRAGMA table_info({table})")
        columns = [r[1] for r in sqlite_cur.fetchall()]
        all_data[table] = {
            'columns': columns,
            'rows': [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
        }
        print(f"  📊 {table}: {len(rows)} filas")

    sqlite_conn.close()

    # 4. Crear tablas en MySQL
    print("\n🏗️  Creando tablas en MySQL...")
    create_tables_in_mysql()

    # 5. Migrar datos en orden (respetando FK)
    print("\n📤 Migrando datos a MySQL...")
    table_order = ['usuarios', 'departamentos', 'guiones', 'eventos',
                   'sincronizaciones', 'guion_fechas', 'eventos_sincronizados', 'elementos_guion']

    for table in table_order:
        if table in all_data and all_data[table]['rows']:
            migrate_table(table, all_data[table]['columns'], all_data[table]['rows'])

    print("\n" + "=" * 50)
    print("✅ Migración completada!")
    print("Ejecuta: python3 run.py")
    print("=" * 50)


if __name__ == '__main__':
    main()
