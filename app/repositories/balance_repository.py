from app.repositories.base_repository import BaseRepository
from app.models.balance import Pago


class BalanceRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def obtener_contratos_activos(self):
        sql = """
            SELECT c.id_contrato, c.monto_total, c.estado as contrato_estado,
                   COALESCE(p.nombre_empresa, 'Sin patrocinador') as nombre_patrocinador
            FROM contrato c
            LEFT JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador
            WHERE c.estado = 1
            ORDER BY c.id_contrato
        """
        return self.fetch_all(sql)

    def obtener_contrato_por_id(self, id_contrato):
        row = self.fetch_one("""
            SELECT c.id_contrato, c.monto_total,
                   COALESCE(p.nombre_empresa, 'Sin patrocinador') as nombre_patrocinador
            FROM contrato c
            LEFT JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador
            WHERE c.id_contrato = %s
        """, (id_contrato,))
        return row

    def registrar_pago(self, datos):
        id = self.execute("""
            INSERT INTO pagos (id_contrato, monto, tipo_pago, referencia,
                               fecha_pago, hora_pago, registrado_por,
                               Descripción, estado, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, NOW())
        """, (
            datos['id_contrato'], datos['monto'], datos['tipo_pago'],
            datos.get('referencia'), datos['fecha_pago'], datos['hora_pago'],
            datos.get('registrado_por'), datos.get('Descripción'),
        ))
        return self.obtener_pago_por_id(id)

    def get_total_pagado_by_contrato(self, id_contrato):
        row = self.fetch_one(
            "SELECT COALESCE(SUM(monto), 0) as total FROM pagos WHERE id_contrato = %s AND estado = 0",
            (id_contrato,)
        )
        return float(row['total']) if row else 0.0

    def get_total_pagado_general(self):
        row = self.fetch_one(
            "SELECT COALESCE(SUM(monto), 0) as total FROM pagos WHERE estado = 0"
        )
        return float(row['total']) if row else 0.0

    def get_historial_pagos(self, limit=100):
        rows = self.fetch_all("""
            SELECT p.*, COALESCE(pat.nombre_empresa, 'Sin patrocinador') as nombre_patrocinador
            FROM pagos p
            LEFT JOIN contrato c ON p.id_contrato = c.id_contrato
            LEFT JOIN patrocinadores pat ON c.id_patrocinador = pat.id_patrocinador
            WHERE p.estado = 0
            ORDER BY p.fecha_registro DESC
            LIMIT %s
        """, (limit,))
        return [Pago(**r) for r in rows]

    def obtener_pago_por_id(self, id_pago):
        row = self.fetch_one("""
            SELECT p.*, COALESCE(pat.nombre_empresa, 'Sin patrocinador') as nombre_patrocinador
            FROM pagos p
            LEFT JOIN contrato c ON p.id_contrato = c.id_contrato
            LEFT JOIN patrocinadores pat ON c.id_patrocinador = pat.id_patrocinador
            WHERE p.id_pago = %s
        """, (id_pago,))
        return Pago(**row) if row else None

    def obtener_top_contratos(self, limit=5):
        return self.fetch_all("""
            SELECT p.id_contrato, COUNT(*) as total_pagos,
                   COALESCE(pat.nombre_empresa, 'Sin patrocinador') as nombre_patrocinador
            FROM pagos p
            JOIN contrato c ON p.id_contrato = c.id_contrato
            LEFT JOIN patrocinadores pat ON c.id_patrocinador = pat.id_patrocinador
            WHERE p.estado = 0
            GROUP BY p.id_contrato
            ORDER BY total_pagos DESC
            LIMIT %s
        """, (limit,))

    def modificar_pago(self, pago_id, datos):
        pago = self.obtener_pago_por_id(pago_id)
        if not pago:
            return None
        sets = []
        params = []
        for campo in ['monto', 'tipo_pago', 'referencia', 'fecha_pago',
                       'hora_pago', 'Descripción']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(pago_id)
            self.execute(
                f"UPDATE pagos SET {', '.join(sets)} WHERE id_pago = %s",
                params
            )
        return self.obtener_pago_por_id(pago_id)

    def eliminar_pago(self, pago_id):
        pago = self.obtener_pago_por_id(pago_id)
        if not pago:
            return None
        self.execute("UPDATE pagos SET estado = 1 WHERE id_pago = %s", (pago_id,))
        return pago
