from app.repositories.base_repository import BaseRepository
from app.models.premio import Patrocinador


class PatrocinadorRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, activos=True):
        sql = "SELECT * FROM patrocinadores"
        params = []
        if activos:
            sql += " WHERE estado = 1"
        sql += " ORDER BY nombre_empresa ASC"
        rows = self.fetch_all(sql, params)
        return [Patrocinador(**r) for r in rows]

    def obtener_por_id(self, id_patrocinador):
        row = self.fetch_one(
            "SELECT * FROM patrocinadores WHERE id_patrocinador = %s",
            (id_patrocinador,)
        )
        return Patrocinador(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO patrocinadores
               (nombre_empresa, rif, tipo_contrato, nombre_contacto, telefono, email, estado)
               VALUES (%s, %s, %s, %s, %s, %s, 1)""",
            (
                datos['nombre_empresa'],
                datos['rif'],
                datos.get('tipo_contrato', 1),
                datos['nombre_contacto'],
                datos['telefono'],
                datos['email'],
            )
        )
        return self.obtener_por_id(id)

    def modificar(self, id_patrocinador, datos):
        sets = []
        params = []
        for campo in ['nombre_empresa', 'rif', 'tipo_contrato', 'nombre_contacto', 'telefono', 'email']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_patrocinador)
            self.execute(
                f"UPDATE patrocinadores SET {', '.join(sets)} WHERE id_patrocinador = %s",
                params
            )
        return self.obtener_por_id(id_patrocinador)

    def eliminar(self, id_patrocinador):
        patrocinador = self.obtener_por_id(id_patrocinador)
        if not patrocinador:
            return None
        self.execute(
            "UPDATE patrocinadores SET estado = 0 WHERE id_patrocinador = %s",
            (id_patrocinador,)
        )
        return patrocinador
