# app/traits/validaciones.py
# Mixin de validación — equivalente al trait Validaciones.php

import re
import html


class ValidacionesMixin:
    """Mixin reutilizable con métodos de validación tipo PHP trait"""

    errores: list = []

    def validar_obligatorios(self, campos: list, datos: dict) -> bool:
        valido = True
        for campo in campos:
            if not datos.get(campo):
                self.errores.append(f"El campo {campo} es obligatorio")
                valido = False
        return valido

    def validar_longitud(self, texto, min_len: int, max_len: int, campo: str) -> bool:
        largo = len(str(texto).strip())
        if largo < min_len:
            self.errores.append(f"{campo} debe tener al menos {min_len} caracteres")
            return False
        if largo > max_len:
            self.errores.append(f"{campo} no puede tener más de {max_len} caracteres")
            return False
        return True

    def validar_fecha(self, fecha_str: str, campo: str = 'fecha') -> bool:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_str):
            self.errores.append(f"Formato de {campo} debe ser YYYY-MM-DD")
            return False
        return True

    def validar_hora(self, hora_str: str, campo: str = 'hora') -> bool:
        if not re.match(r'^\d{2}:\d{2}$', hora_str):
            self.errores.append(f"Formato de {campo} debe ser HH:MM")
            return False
        return True

    def validar_numero_positivo(self, valor, campo: str) -> bool:
        try:
            num = int(valor)
            if num <= 0:
                self.errores.append(f"{campo} debe ser un número positivo")
                return False
        except (ValueError, TypeError):
            self.errores.append(f"{campo} debe ser un número válido")
            return False
        return True

    def validar_email(self, email: str, campo: str = 'email') -> bool:
        patron = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
        if not re.match(patron, email):
            self.errores.append(f"{campo} no tiene un formato válido")
            return False
        return True

    def validar_cedula(self, cedula: str, campo: str = 'cédula') -> bool:
        if not re.match(r'^[0-9]{6,10}$', str(cedula)):
            self.errores.append(f"{campo} debe tener entre 6 y 10 dígitos")
            return False
        return True

    def validar_telefono(self, telefono: str, campo: str = 'teléfono') -> bool:
        if telefono and not re.match(r'^[0-9]{10,11}$', str(telefono)):
            self.errores.append(f"{campo} debe tener 10 u 11 dígitos")
            return False
        return True

    def validar_rif(self, rif: str, campo: str = 'RIF') -> bool:
        if not re.match(r'^[JGVE]-[0-9]{8,9}$', str(rif).strip()):
            self.errores.append(f"{campo} debe tener formato J/G/E/V-12345678")
            return False
        return True

    def validar_texto_seguro(self, texto: str, campo: str) -> bool:
        if re.search(r'[<>\"\'\{\}\(\)\&\$\%\#\@\*\=\[\]\;\/\\\|\`\~]', str(texto)):
            self.errores.append(f"{campo} contiene caracteres no permitidos")
            return False
        return True

    def sanitizar_texto(self, texto: str) -> str:
        if texto is None:
            return ''
        return html.escape(str(texto).strip())

    def get_errores(self) -> list:
        return self.errores

    def limpiar_errores(self):
        self.errores = []

    def tiene_errores(self) -> bool:
        return bool(self.errores)
