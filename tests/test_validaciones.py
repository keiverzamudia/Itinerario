"""Tests de validaciones puras — sin BD, sin app."""
from app.model.validaciones_model import ValidacionesMixin


class V(ValidacionesMixin):
    pass


def _nuevo():
    return V()


def test_obligatorio_rechaza_vacio_y_espacios():
    v = _nuevo()
    assert not v.validar_obligatorio('', 'x')
    assert not v.validar_obligatorio('   ', 'x')
    assert not v.validar_obligatorio(None, 'x')
    assert v.validar_obligatorio('dato', 'x')


def test_obligatorios_acumula_errores():
    v = _nuevo()
    assert not v.validar_obligatorios(['a', 'b'], {'a': 'ok'})
    assert len(v.get_errores()) == 1
    # 0 y False cuentan como presentes
    assert v.validar_obligatorios(['cero'], {'cero': 0})


def test_entero_positivo():
    v = _nuevo()
    assert v.validar_entero_positivo('5', 'n')
    assert not v.validar_entero_positivo(0, 'n')
    assert not v.validar_entero_positivo(-3, 'n')
    assert not v.validar_entero_positivo('abc', 'n')
    assert not v.validar_entero_positivo(None, 'n')


def test_fecha_formato_y_realidad():
    v = _nuevo()
    assert v.validar_fecha('2024-01-15')
    assert not v.validar_fecha('15/01/2024')      # formato incorrecto
    assert not v.validar_fecha('2024-02-30')      # fecha inexistente
    assert not v.validar_fecha(None)


def test_texto_prohibido_y_sanitizacion():
    v = _nuevo()
    assert not v.validar_texto('<script>', 'campo')
    assert v.validar_texto('Texto normal 123', 'campo')
    # elimina < > / y recorta bordes (comportamiento actual)
    assert ValidacionesMixin.sanitizar_texto(" <b>hola</b> ") == 'bholab'


def test_longitud():
    v = _nuevo()
    assert v.validar_longitud('abc', 1, 10, 'campo')
    assert not v.validar_longitud('', 1, 10, 'campo')
    assert not v.validar_longitud('x' * 11, 1, 10, 'campo')
