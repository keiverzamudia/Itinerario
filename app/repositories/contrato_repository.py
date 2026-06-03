from app.repositories.base_repository import BaseRepository
from app.models.contrato import Contrato


class ContratoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, activos=True):
        sql = """SELECT c.*, p.nombre_empresa
                 FROM contrato c
                 LEFT JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador"""
        params = []
        if activos:
            sql += " WHERE c.estado = 1"
        sql += " ORDER BY c.fecha_inicio DESC"
        rows = self.fetch_all(sql, params)
        return [Contrato(**r) for r in rows]

    def obtener_por_id(self, id_contrato):
        row = self.fetch_one(
            """SELECT c.*, p.nombre_empresa
               FROM contrato c
               LEFT JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador
               WHERE c.id_contrato = %s""",
            (id_contrato,)
        )
        return Contrato(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO contrato
               (id_patrocinador, fecha_inicio, fecha_fin, estado, estatus, tipo, monto_total)
               VALUES (%s, %s, %s, 1, %s, %s, %s)""",
            (
                datos['id_patrocinador'],
                datos['fecha_inicio'],
                datos['fecha_fin'],
                datos.get('estatus', 'Borrador'),
                datos['tipo'],
                datos.get('monto_total'),
            )
        )
        return self.obtener_por_id(id)

    def modificar(self, id_contrato, datos):
        sets = []
        params = []
        for campo in ['id_patrocinador', 'fecha_inicio', 'fecha_fin',
                       'estatus', 'tipo', 'monto_total']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_contrato)
            self.execute(
                f"UPDATE contrato SET {', '.join(sets)} WHERE id_contrato = %s",
                params
            )
        return self.obtener_por_id(id_contrato)

    def eliminar(self, id_contrato):
        contrato = self.obtener_por_id(id_contrato)
        if not contrato:
            return None
        self.execute(
            "UPDATE contrato SET estado = 0 WHERE id_contrato = %s",
            (id_contrato,)
        )
        return contrato
