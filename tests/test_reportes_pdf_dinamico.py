"""Tests del motor de reportes PDF dinámico."""
import pytest


class FakeUser:
    def __init__(self):
        self.nombre = 'Test User'
        self.rol = 'Admin'
        self.departamento = 'IT'


class TestOpcionales:
    """Generadores funcionan sin opciones (comportamiento heredado)."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_contratos_sin_opciones(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'tipo': 'Oro', 'estatus': 'Vigente',
                  'fecha_inicio': '2024-01-01', 'fecha_fin': '2025-01-01',
                  'dias_restantes': 30, 'monto_total': 50000}]
        pdf = gen.generate(datos, filtros={'año': '2024'}, kpis={'oro': 1})
        assert len(pdf) > 1000
        assert pdf[:4] == b'%PDF'

    def test_inventario_sin_opciones(self, app):
        from app.helpers.generators.inventario_report import InventarioReport
        gen = InventarioReport(self.usuario)
        datos = [{'id': 1, 'nombre': 'Bola', 'tipo_nombre': 'Deportivo',
                  'estado_nombre': 'Bueno', 'fecha_compra': '2024-01-01'}]
        pdf = gen.generate(datos, kpis={'tipos': {'Deportivo': 1}})
        assert pdf[:4] == b'%PDF'

    def test_premios_sin_opciones(self, app):
        from app.helpers.generators.premios_report import PremiosReport
        gen = PremiosReport(self.usuario)
        datos = [{'nombre': 'Gorra', 'patrocinador_nombre': 'Nike',
                  'estado': 'Entregado', 'cantidad': 10, 'cantidad_entregada': 8,
                  'fecha_creacion': '2024-06-01'}]
        pdf = gen.generate(datos, kpis={'pendientes': 2, 'entregados': 8})
        assert pdf[:4] == b'%PDF'

    def test_guiones_sin_opciones(self, app):
        from app.helpers.generators.guiones_report import GuionesReport
        gen = GuionesReport(self.usuario)
        datos = [{'nombre': 'Show #1', 'game': 5, 'pregame': 3,
                  'fecha_ejecucion': '2024-07-01', 'estado': 'Publicado',
                  'tiempo_total': '45m'}]
        pdf = gen.generate(datos, kpis={'publicados': 1})
        assert pdf[:4] == b'%PDF'

    def test_balance_sin_opciones(self, app):
        from app.helpers.generators.balance_report import BalanceReport
        gen = BalanceReport(self.usuario)
        datos = [{'nombre_patrocinador': 'Banco X', 'tipo_pago': 'Efectivo',
                  'monto': 10000, 'referencia': 'REF001', 'fecha_pago': '2024-08-01'}]
        pdf = gen.generate(datos)
        assert pdf[:4] == b'%PDF'

    def test_tareas_sin_opciones(self, app):
        from app.helpers.generators.tareas_report import TareasReport
        gen = TareasReport(self.usuario)
        datos = [{'nombre_tarea': 'Limpieza', 'estado': 'Pendiente',
                  'asignado_a': 'Juan', 'fecha_asignacion_tarea': '2024-09-01'}]
        pdf = gen.generate(datos, kpis={'pendientes': 1})
        assert pdf[:4] == b'%PDF'

    def test_patrocinadores_sin_opciones(self, app):
        from app.helpers.generators.patrocinadores_report import PatrocinadoresReport
        gen = PatrocinadoresReport(self.usuario)
        datos = [{'nombre_empresa': 'PepsiCo', 'rif': 'J-12345678',
                  'telefono': '0212-1234567', 'tipo_contrato': 'Oro'}]
        pdf = gen.generate(datos)
        assert pdf[:4] == b'%PDF'

    def test_usuarios_sin_opciones(self, app):
        from app.helpers.generators.usuarios_report import UsuariosReport
        gen = UsuariosReport(self.usuario)
        datos = [{'nombre': 'Maria', 'email': 'maria@test.com', 'rol': 'Admin',
                  'departamento': 'IT', 'activo': 1}]
        pdf = gen.generate(datos)
        assert pdf[:4] == b'%PDF'

    def test_mantenimiento_sin_opciones(self, app):
        from app.helpers.generators.mantenimiento_report import MantenimientoReport
        gen = MantenimientoReport(self.usuario)
        datos = [{'recurso_nombre': 'Display LED', 'estado': 'En reparación',
                  'fecha_ingreso': '2024-10-01', 'diagnostico': 'Falla pixel'}]
        pdf = gen.generate(datos, kpis={'en_reparacion': 1})
        assert pdf[:4] == b'%PDF'

    def test_bitacora_sin_opciones(self, app):
        from app.helpers.generators.bitacora_report import BitacoraReport
        gen = BitacoraReport(self.usuario)
        datos = [{'id': 1, 'usuario_nombre': 'Admin', 'tipo_accion': 'Creación',
                  'modulo': 'Inventario', 'accion': 'Crear equipo',
                  'created_at': '2024-11-01 10:00:00'}]
        pdf = gen.generate(datos, kpis={'creaciones': 1})
        assert pdf[:4] == b'%PDF'


class TestColumnasDinamicas:
    """Generadores con columnas seleccionadas dinámicamente."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_contratos_una_columna(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'monto_total': 50000}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': ['nombre_empresa']})
        assert pdf[:4] == b'%PDF'

    def test_contratos_varias_columnas(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'tipo': 'Oro', 'monto_total': 50000}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': ['nombre_empresa', 'tipo', 'monto_total']})
        assert pdf[:4] == b'%PDF'

    def test_inventario_todas_las_columnas(self, app):
        from app.helpers.generators.inventario_report import InventarioReport
        from app.helpers.reportes_campos import CAMPOS_DISPONIBLES
        gen = InventarioReport(self.usuario)
        campos = list(CAMPOS_DISPONIBLES['inventario'].keys())
        datos = [{'id': 1, 'nombre': 'Bola'}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': campos})
        assert pdf[:4] == b'%PDF'

    def test_columnas_invalidas_se_descartan(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': ['campo_falso', 'otro_falso']})
        assert pdf[:4] == b'%PDF'


class TestAgrupacion:
    """Tabla agrupada con subtotales."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_agrupar_por_estado(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [
            {'nombre_empresa': 'A', 'tipo': 'Oro', 'monto_total': 10000},
            {'nombre_empresa': 'B', 'tipo': 'Plata', 'monto_total': 5000},
            {'nombre_empresa': 'C', 'tipo': 'Oro', 'monto_total': 8000},
        ]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_empresa', 'tipo', 'monto_total'],
            'agrupar_por': 'tipo'
        })
        assert pdf[:4] == b'%PDF'


class TestOrientacion:
    """Orientación automática."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_orientacion_horizontal(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_empresa'],
            'orientacion': 'horizontal'
        })
        assert pdf[:4] == b'%PDF'


class TestPostTableSections:
    """Hook de distribuciones funciona."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_contratos_distribuciones(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme'}]
        kpis = {'oro': 3, 'plata': 2, 'vigentes': 4, 'vencidos': 1}
        pdf = gen.generate(datos, kpis=kpis)
        assert pdf[:4] == b'%PDF'

    def test_tareas_distribuciones(self, app):
        from app.helpers.generators.tareas_report import TareasReport
        gen = TareasReport(self.usuario)
        datos = [{'nombre_tarea': 'X'}]
        kpis = {'pendientes': 5, 'completadas': 3}
        pdf = gen.generate(datos, kpis=kpis)
        assert pdf[:4] == b'%PDF'

    def test_mantenimiento_distribuciones(self, app):
        from app.helpers.generators.mantenimiento_report import MantenimientoReport
        gen = MantenimientoReport(self.usuario)
        datos = [{'recurso_nombre': 'Y'}]
        kpis = {'en_espera': 2, 'reparados': 4}
        pdf = gen.generate(datos, kpis=kpis)
        assert pdf[:4] == b'%PDF'


class TestReels:
    """Reels mantiene su layout custom."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_reels_con_datos(self, app):
        from app.helpers.generators.reels_report import ReelsReport
        gen = ReelsReport(self.usuario)
        datos = [{
            'nombre': 'Reel #1',
            'patrocinado': 'Sponsor',
            'duracion': '2:30',
            'creado_en': '2024-01-15',
            'videos': [
                {'nombre': 'Video 1', 'duracion_segundos': 60, 'patrocinador_nombre': 'Nike'}
            ]
        }]
        pdf = gen.generate(datos, kpis={'total_reels': 1, 'total_videos': 1})
        assert pdf[:4] == b'%PDF'

    def test_reels_vacio(self, app):
        from app.helpers.generators.reels_report import ReelsReport
        gen = ReelsReport(self.usuario)
        pdf = gen.generate([], kpis={})
        assert pdf[:4] == b'%PDF'


class TestValidacion:
    """Validación server-side de opciones."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_columnas_invalidas_se_ignoran(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': ['no_existe', 'tampoco']})
        assert pdf[:4] == b'%PDF'

    def test_orientacion_invalida_se_ignora(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={'orientacion': 'diagonal'})
        assert pdf[:4] == b'%PDF'

    def test_agrupar_por_invalido_se_ignora(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'monto_total': 1000}]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_empresa', 'monto_total'],
            'agrupar_por': 'campo_falso'
        })
        assert pdf[:4] == b'%PDF'

    def test_opciones_vacias_usa_default(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'monto_total': 1000}]
        pdf = gen.generate(datos, opciones={})
        assert pdf[:4] == b'%PDF'


class TestOrdenamiento:
    """Ordenamiento dinámico de datos."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_ordenar_por_nombre(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [
            {'nombre_empresa': 'Charlie', 'monto_total': 3000},
            {'nombre_empresa': 'Alpha', 'monto_total': 1000},
            {'nombre_empresa': 'Bravo', 'monto_total': 2000},
        ]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_empresa', 'monto_total'],
            'ordenar_por': 'nombre_empresa'
        })
        assert pdf[:4] == b'%PDF'

    def test_ordenar_por_monto(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [
            {'nombre_empresa': 'A', 'monto_total': 3000},
            {'nombre_empresa': 'B', 'monto_total': 1000},
            {'nombre_empresa': 'C', 'monto_total': 2000},
        ]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_empresa', 'monto_total'],
            'ordenar_por': 'monto_total'
        })
        assert pdf[:4] == b'%PDF'


class TestMultiplesColumnas:
    """PDF con distintas cantidades de columnas."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_una_sola_columna(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': ['nombre_empresa']})
        assert pdf[:4] == b'%PDF'

    def test_cinco_columnas(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'tipo': 'Oro', 'estatus': 'Vigente',
                  'monto_total': 50000, 'dias_restantes': 30}]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_empresa', 'tipo', 'estatus', 'monto_total', 'dias_restantes']
        })
        assert pdf[:4] == b'%PDF'

    def test_diez_columnas(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        from app.helpers.reportes_campos import CAMPOS_DISPONIBLES
        gen = ContratosReport(self.usuario)
        campos = list(CAMPOS_DISPONIBLES['contratos'].keys())[:10]
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': campos})
        assert pdf[:4] == b'%PDF'

    def test_todas_las_columnas_contratos(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        from app.helpers.reportes_campos import CAMPOS_DISPONIBLES
        gen = ContratosReport(self.usuario)
        campos = list(CAMPOS_DISPONIBLES['contratos'].keys())
        datos = [{'nombre_empresa': 'Acme'}]
        pdf = gen.generate(datos, opciones={'columnas_seleccionadas': campos})
        assert pdf[:4] == b'%PDF'


class TestAgrupacionSubtotales:
    """Agrupación con subtotales en diferentes módulos."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_agrupar_inventario_por_tipo(self, app):
        from app.helpers.generators.inventario_report import InventarioReport
        gen = InventarioReport(self.usuario)
        datos = [
            {'nombre': 'Bola', 'tipo_nombre': 'Deportivo', 'costo': 100},
            {'nombre': 'Silla', 'tipo_nombre': 'Mobiliario', 'costo': 200},
            {'nombre': 'Red', 'tipo_nombre': 'Deportivo', 'costo': 50},
        ]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre', 'tipo_nombre', 'costo'],
            'agrupar_por': 'tipo_nombre'
        })
        assert pdf[:4] == b'%PDF'

    def test_agrupar_tareas_por_estado(self, app):
        from app.helpers.generators.tareas_report import TareasReport
        gen = TareasReport(self.usuario)
        datos = [
            {'nombre_tarea': 'T1', 'estado': 'Pendiente', 'asignado_a': 'A'},
            {'nombre_tarea': 'T2', 'estado': 'Completada', 'asignado_a': 'B'},
            {'nombre_tarea': 'T3', 'estado': 'Pendiente', 'asignado_a': 'C'},
        ]
        pdf = gen.generate(datos, opciones={
            'columnas_seleccionadas': ['nombre_tarea', 'estado', 'asignado_a'],
            'agrupar_por': 'estado'
        })
        assert pdf[:4] == b'%PDF'


class TestAnalisisCompleto:
    """Resumen ejecutivo + Top-N + comparativa."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.usuario = FakeUser()

    def test_resumen_ejecutivo(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'monto_total': 50000}]
        kpis = {'total': 10, 'vigentes': 7, 'monto_total': '$500,000'}
        pdf = gen.generate(datos, kpis=kpis, opciones={'resumen': True})
        assert pdf[:4] == b'%PDF'

    def test_top_n(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': f'Empresa {i}', 'monto_total': i * 1000} for i in range(10)]
        kpis = {'total': 10}
        pdf = gen.generate(datos, kpis=kpis, opciones={'top_n': 3})
        assert pdf[:4] == b'%PDF'

    def test_comparativa(self, app):
        from app.helpers.generators.contratos_report import ContratosReport
        gen = ContratosReport(self.usuario)
        datos = [{'nombre_empresa': 'Acme', 'monto_total': 50000}]
        kpis = {'total': 10, 'kpis_previos': {'total': 8}}
        pdf = gen.generate(datos, kpis=kpis, opciones={'comparar': True, 'kpis_previos': {'total': 8}})
        assert pdf[:4] == b'%PDF'
