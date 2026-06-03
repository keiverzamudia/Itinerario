from app.repositories.base_repository import BaseRepository
from app.models.usuario import Usuario


class UsuarioRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def _row_to_usuario(self, row):
        return Usuario(**row) if row else None

    def consultar(self, **filtros):
        sql = "SELECT * FROM usuarios WHERE 1=1"
        params = []
        if filtros.get('rol'):
            sql += " AND rol = %s"
            params.append(filtros['rol'])
        if filtros.get('activo') is not None:
            sql += " AND activo = %s"
            params.append(1 if filtros['activo'] else 0)
        sql += " ORDER BY nombre ASC"
        rows = self.fetch_all(sql, params)
        return [Usuario(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM usuarios WHERE id = %s", (id,))
        return self._row_to_usuario(row)

    def obtener_por_email(self, email):
        row = self.fetch_one("SELECT * FROM usuarios WHERE email = %s", (email,))
        return self._row_to_usuario(row)

    def contar(self, **filtros):
        sql = "SELECT COUNT(*) as total FROM usuarios WHERE 1=1"
        params = []
        if filtros.get('rol'):
            sql += " AND rol = %s"
            params.append(filtros['rol'])
        row = self.fetch_one(sql, params)
        return row['total'] if row else 0

    def registrar(self, datos):
        from pymysql.err import IntegrityError
        try:
            sql = """INSERT INTO usuarios (nombre, email, password_hash, cedula, rol,
                     departamento, telefono, activo, fecha_registro)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())"""
            id = self.execute(sql, (
                datos['nombre'], datos['email'], datos['password_hash'],
                datos['cedula'], datos.get('rol', 'Usuario'),
                datos.get('departamento', 'Medios'), datos.get('telefono', ''),
                1,
            ))
            return self.obtener_por_id(id)
        except IntegrityError:
            return None

    def modificar(self, id, datos):
        sets = []
        params = []
        for campo in ['nombre', 'email', 'rol', 'departamento', 'telefono',
                      'password_hash', 'activo']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            sql = f"UPDATE usuarios SET {', '.join(sets)} WHERE id = %s"
            params.append(id)
            self.execute(sql, params)
        return self.obtener_por_id(id)

    def eliminar(self, id):
        self.execute("DELETE FROM usuarios WHERE id = %s", (id,))

    def actualizar_ultimo_acceso(self, id):
        self.execute(
            "UPDATE usuarios SET ultimo_acceso = NOW() WHERE id = %s",
            (id,)
        )
