"""Tests para reportes_campos.py - definiciones de campos y formatters."""
import pytest
from app.helpers.reportes_campos import (
    CAMPOS_DISPONIBLES, COLUMNAS_DEFAULT, FORMATTERS, CAMPOS_NUMERICOS,
    _fmt_texto, _fmt_texto_largo, _fmt_entero, _fmt_moneda, _fmt_decimal,
    _fmt_fecha, _fmt_fecha_hora, _fmt_duracion, _fmt_porcentaje, _fmt_boolean,
)


# ---------------------------------------------------------------------------
# Tests de formatters
# ---------------------------------------------------------------------------

class TestFormatters:
    def test_texto_normal(self):
        assert _fmt_texto('hola') == 'hola'

    def test_texto_none(self):
        assert _fmt_texto(None) == '—'

    def test_texto_largo_corto(self):
        assert _fmt_texto_largo('corto') == 'corto'

    def test_texto_largo_largo(self):
        largo = 'x' * 60
        assert _fmt_texto_largo(largo).endswith('..')
        assert len(_fmt_texto_largo(largo)) == 52

    def test_entero(self):
        assert _fmt_entero(1234) == '1,234'

    def test_entero_none(self):
        assert _fmt_entero(None) == '0'

    def test_moneda(self):
        assert _fmt_moneda(12345.67) == '$12,345.67'

    def test_moneda_none(self):
        assert _fmt_moneda(None) == '$0.00'

    def test_decimal(self):
        assert _fmt_decimal(12.3) == '12.3'

    def test_fecha(self):
        assert _fmt_fecha('2026-01-15') == '2026-01-15'

    def test_fecha_none(self):
        assert _fmt_fecha(None) == '—'

    def test_fecha_hora(self):
        assert _fmt_fecha_hora('2026-01-15 14:30:00') == '2026-01-15 14:30'

    def test_duracion_segundos(self):
        assert _fmt_duracion(45) == '45s'

    def test_duracion_minutos(self):
        assert _fmt_duracion(125) == '2m 5s'

    def test_duracion_horas(self):
        assert _fmt_duracion(3661) == '1h 1m'

    def test_duracion_none(self):
        assert _fmt_duracion(None) == '—'

    def test_porcentaje(self):
        assert _fmt_porcentaje(85.5) == '85.5%'

    def test_boolean_true(self):
        assert _fmt_boolean(True) == 'Si'

    def test_boolean_false(self):
        assert _fmt_boolean(False) == 'No'


# ---------------------------------------------------------------------------
# Tests de estructura de campos
# ---------------------------------------------------------------------------

class TestCamposEstructura:
    @pytest.mark.parametrize("modulo", CAMPOS_DISPONIBLES.keys())
    def test_cada_modulo_tiene_campos(self, modulo):
        campos = CAMPOS_DISPONIBLES[modulo]
        assert len(campos) > 0, f"Modulo {modulo} no tiene campos"

    @pytest.mark.parametrize("modulo", CAMPOS_DISPONIBLES.keys())
    def test_cada_campo_tiene_propiedades_requeridas(self, modulo):
        for key, campo in CAMPOS_DISPONIBLES[modulo].items():
            assert 'label' in campo, f"{modulo}.{key} sin label"
            assert 'type' in campo, f"{modulo}.{key} sin type"
            assert 'width' in campo, f"{modulo}.{key} sin width"
            assert 'order' in campo, f"{modulo}.{key} sin order"
            assert campo['type'] in FORMATTERS, f"{modulo}.{key} type '{campo['type']}' no tiene formatter"

    @pytest.mark.parametrize("modulo", CAMPOS_DISPONIBLES.keys())
    def test_keys_unicos_por_modulo(self, modulo):
        campos = CAMPOS_DISPONIBLES[modulo]
        keys = list(campos.keys())
        assert len(keys) == len(set(keys)), f"Modulo {modulo} tiene keys duplicados"


# ---------------------------------------------------------------------------
# Tests de COLUMNAS_DEFAULT
# ---------------------------------------------------------------------------

class TestColumnasDefault:
    @pytest.mark.parametrize("modulo", COLUMNAS_DEFAULT.keys())
    def test_defaults_existen_en_campos(self, modulo):
        defaults = COLUMNAS_DEFAULT[modulo]
        campos = CAMPOS_DISPONIBLES[modulo]
        for key in defaults:
            assert key in campos, f"Default '{key}' no existe en CAMPOS_DISPONIBLES[{modulo}]"

    @pytest.mark.parametrize("modulo", COLUMNAS_DEFAULT.keys())
    def test_defaults_no_vacios(self, modulo):
        assert len(COLUMNAS_DEFAULT[modulo]) > 0, f"Modulo {modulo} sin defaults"

    @pytest.mark.parametrize("modulo", COLUMNAS_DEFAULT.keys())
    def test_defaults_ordenados_por_order(self, modulo):
        defaults = COLUMNAS_DEFAULT[modulo]
        campos = CAMPOS_DISPONIBLES[modulo]
        orders = [campos[k]['order'] for k in defaults]
        assert orders == sorted(orders), f"Defaults de {modulo} no estan en orden de 'order'"


# ---------------------------------------------------------------------------
# Tests de CAMPOS_NUMERICOS
# ---------------------------------------------------------------------------

class TestCamposNumericos:
    def test_tipos_numericos_definidos(self):
        assert 'entero' in CAMPOS_NUMERICOS
        assert 'moneda' in CAMPOS_NUMERICOS
        assert 'decimal' in CAMPOS_NUMERICOS
        assert 'porcentaje' in CAMPOS_NUMERICOS

    def test_tipos_no_numericos_excluidos(self):
        assert 'texto' not in CAMPOS_NUMERICOS
        assert 'fecha' not in CAMPOS_NUMERICOS


# ---------------------------------------------------------------------------
# Tests de todos los modulos cubiertos
# ---------------------------------------------------------------------------

class TestCobertura:
    MODULOS_ESPERADOS = {
        'guiones', 'inventario', 'premios', 'contratos', 'balance',
        'tareas', 'patrocinadores', 'usuarios', 'mantenimiento', 'reels', 'bitacora',
    }

    def test_modulos_cubiertos(self):
        assert set(CAMPOS_DISPONIBLES.keys()) == self.MODULOS_ESPERADOS

    def test_defaults_cubiertos(self):
        assert set(COLUMNAS_DEFAULT.keys()) == self.MODULOS_ESPERADOS
