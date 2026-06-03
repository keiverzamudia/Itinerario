from datetime import datetime, timezone, date
from app.repositories.base_repository import BaseRepository
from app.models.premio import Premio, Patrocinador


class PremioRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, **filtros):
        sql = "SELECT * FROM premios WHERE estatus = FALSE"
        params = []
        if filtros.get('estado'):
            sql += " AND estado = %s"
            params.append(filtros['estado'])
        sql += " ORDER BY fecha_creacion DESC, hora_creacion DESC"
        rows = self.fetch_all(sql, params)
        return [Premio(**r) for r in rows]

    def contar(self, **filtros):
        sql = "SELECT COUNT(*) as total FROM premios WHERE estatus = FALSE"
        params = []
        if filtros.get('estado'):
            sql += " AND estado = %s"
            params.append(filtros['estado'])
        row = self.fetch_one(sql, params)
        return row['total'] if row else 0

    def obtener_por_id(self, id_registro):
        row = self.fetch_one(
            "SELECT * FROM premios WHERE id = %s AND estatus = FALSE",
            (id_registro,)
        )
        return Premio(**row) if row else None

    def registrar(self, datos):
        self.execute(
            """INSERT INTO premios
               (nombre, id_patrocinador, descripcion, estado,
                fecha_creacion, hora_creacion, foto, estatus)
               VALUES (%s, %s, %s, 'pendiente',
                %s, %s, %s, FALSE)""",
            (
                datos['nombre'],
                datos.get('id_patrocinador'),
                datos.get('descripcion'),
                datos.get('fecha_creacion', date.today()),
                datos.get('hora_creacion', datetime.now().time()),
                datos.get('foto', 'default-premio.png'),
            )
        )

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        for campo in ['nombre', 'id_patrocinador', 'descripcion', 'foto']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_registro)
            self.execute(f"UPDATE premios SET {', '.join(sets)} WHERE id = %s", params)

    def eliminar(self, id_registro):
        premio = self.obtener_por_id(id_registro)
        if not premio:
            return None
        self.execute("UPDATE premios SET estatus = TRUE WHERE id = %s", (id_registro,))
        return premio.nombre

    def obtener_premios_pendientes(self):
        rows = self.fetch_all("""
            SELECT p.id, p.nombre, p.descripcion, p.estado, p.id_patrocinador,
                   p.foto, p.fecha_creacion, p.hora_creacion,
                   pat.nombre_empresa as patrocinador_nombre
            FROM premios p
            LEFT JOIN patrocinadores pat ON p.id_patrocinador = pat.id_patrocinador
            WHERE p.estado = 'pendiente' AND p.estatus = FALSE
            ORDER BY p.fecha_creacion DESC, p.hora_creacion DESC
        """)
        return [Premio(**r) for r in rows]

    def obtener_premios_entregados(self):
        rows = self.fetch_all("""
            SELECT p.id, p.nombre, p.descripcion, p.foto, p.fecha_entrega, p.entregado_por,
                   pat.nombre_empresa as patrocinador_nombre
            FROM premios p
            LEFT JOIN patrocinadores pat ON p.id_patrocinador = pat.id_patrocinador
            WHERE p.estado = 'entregado' AND p.estatus = FALSE
            ORDER BY p.fecha_entrega DESC
            LIMIT 100
        """)
        premios = [Premio(**r) for r in rows]
        self._cargar_nombres_usuario(premios)
        return premios

    def _cargar_nombres_usuario(self, premios):
        from app.repositories.usuario_repository import UsuarioRepository
        user_repo = UsuarioRepository()
        for p in premios:
            if p.entregado_por:
                user = user_repo.obtener_por_id(p.entregado_por)
                p.usuario_nombre = user.nombre if user else '—'
            else:
                p.usuario_nombre = '—'

    def obtener_patrocinadores(self):
        rows = self.fetch_all(
            "SELECT id_patrocinador, nombre_empresa FROM patrocinadores ORDER BY nombre_empresa"
        )
        return [Patrocinador(**r) for r in rows]

    def verificar_disponible(self, premio_id):
        row = self.fetch_one(
            "SELECT id, estado, nombre FROM premios WHERE id = %s AND estatus = FALSE",
            (premio_id,)
        )
        return Premio(**row) if row else None

    def obtener_foto_actual(self, premio_id):
        row = self.fetch_one("SELECT foto FROM premios WHERE id = %s", (premio_id,))
        return row['foto'] if row else 'default-premio.png'

    def obtener_para_api(self, premio_id):
        row = self.fetch_one(
            """SELECT id, nombre, id_patrocinador, descripcion, foto
               FROM premios WHERE id = %s AND estatus = FALSE""",
            (premio_id,)
        )
        return Premio(**row) if row else None

    def entregar(self, premio_id, id_patrocinador=None, descripcion=None, entregado_por=None):
        self.execute(
            """UPDATE premios
               SET estado = 'entregado',
                   fecha_entrega = %s,
                   id_patrocinador = %s,
                   descripcion = %s,
                   entregado_por = %s
               WHERE id = %s""",
            (datetime.now(timezone.utc), id_patrocinador, descripcion, entregado_por, premio_id)
        )
