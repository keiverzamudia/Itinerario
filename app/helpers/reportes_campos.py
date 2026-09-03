"""Definicion de campos disponibles para reportes PDF dinamicos.

Cada modulo tiene un dict de campos con metadata para:
- Seleccion en UI (checkboxes)
- Formateo en PDF
- Anchos de columna
- Agrupacion y ordenamiento
"""

# ---------------------------------------------------------------------------
# Formatters por tipo de dato
# ---------------------------------------------------------------------------

def _fmt_texto(v):
    return str(v) if v else '—'

def _fmt_texto_largo(v):
    s = str(v) if v else '—'
    return s[:50] + '..' if len(s) > 50 else s

def _fmt_entero(v):
    try:
        return f"{int(v):,}"
    except (ValueError, TypeError):
        return '0'

def _fmt_moneda(v):
    try:
        return f"${float(v):,.2f}"
    except (ValueError, TypeError):
        return '$0.00'

def _fmt_decimal(v):
    try:
        return f"{float(v):,.1f}"
    except (ValueError, TypeError):
        return '0.0'

def _fmt_fecha(v):
    return str(v) if v else '—'

def _fmt_fecha_hora(v):
    return str(v)[:16] if v else '—'

def _fmt_duracion(v):
    try:
        seg = int(v)
        if seg < 60:
            return f"{seg}s"
        h, r = divmod(seg, 3600)
        m, s = divmod(r, 60)
        return f"{h}h {m}m" if h else f"{m}m {s}s"
    except (ValueError, TypeError):
        return '—'

def _fmt_porcentaje(v):
    try:
        return f"{float(v):.1f}%"
    except (ValueError, TypeError):
        return '0%'

def _fmt_boolean(v):
    return 'Si' if v else 'No'


FORMATTERS = {
    'texto': _fmt_texto,
    'texto_largo': _fmt_texto_largo,
    'entero': _fmt_entero,
    'moneda': _fmt_moneda,
    'decimal': _fmt_decimal,
    'fecha': _fmt_fecha,
    'fecha_hora': _fmt_fecha_hora,
    'duracion': _fmt_duracion,
    'porcentaje': _fmt_porcentaje,
    'boolean': _fmt_boolean,
}

# Tipos que se pueden sumar en subtotales
CAMPOS_NUMERICOS = {'entero', 'moneda', 'decimal', 'porcentaje'}


# ---------------------------------------------------------------------------
# Campos por modulo
# ---------------------------------------------------------------------------
# Estructura: key -> {label, type, width, order, groupable, sortable, aggregate}

CAMPOS_DISPONIBLES = {
    'guiones': {
        'nombre':          {'label': 'Nombre',       'type': 'texto',      'width': 150, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'game':            {'label': 'Game',         'type': 'entero',     'width': 40,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'pregame':         {'label': 'Pre-Game',     'type': 'entero',     'width': 50,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'fecha_ejecucion': {'label': 'Ejecucion',    'type': 'fecha',      'width': 70,  'order': 4,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado':          {'label': 'Estado',        'type': 'texto',      'width': 60,  'order': 5,  'groupable': True,  'sortable': True,  'aggregate': None},
        'tiempo_total':    {'label': 'Tiempo',        'type': 'duracion',   'width': 60,  'order': 6,  'groupable': False, 'sortable': True,  'aggregate': None},
        'creado_en':       {'label': 'Creado',        'type': 'fecha_hora', 'width': 75,  'order': 7,  'groupable': False, 'sortable': True,  'aggregate': None},
        'encargado':       {'label': 'Encargado',     'type': 'texto',      'width': 100, 'order': 8,  'groupable': True,  'sortable': True,  'aggregate': None},
    },
    'inventario': {
        'id':              {'label': 'ID',            'type': 'entero',     'width': 30,  'order': 1,  'groupable': False, 'sortable': True,  'aggregate': None},
        'nombre':          {'label': 'Nombre',        'type': 'texto',      'width': 130, 'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'tipo_nombre':     {'label': 'Tipo',          'type': 'texto',      'width': 80,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado_nombre':   {'label': 'Estado',        'type': 'texto',      'width': 70,  'order': 4,  'groupable': True,  'sortable': True,  'aggregate': None},
        'fecha_compra':    {'label': 'Compra',        'type': 'fecha',      'width': 70,  'order': 5,  'groupable': False, 'sortable': True,  'aggregate': None},
        'costo':           {'label': 'Costo',         'type': 'moneda',     'width': 70,  'order': 6,  'groupable': False, 'sortable': True,  'aggregate': 'suma'},
        'descripcion':     {'label': 'Descripcion',   'type': 'texto_largo','width': 150, 'order': 7,  'groupable': False, 'sortable': False, 'aggregate': None},
    },
    'premios': {
        'nombre':          {'label': 'Nombre',        'type': 'texto',      'width': 120, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'patrocinador':    {'label': 'Patrocinador',  'type': 'texto',      'width': 90,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado':          {'label': 'Estado',        'type': 'texto',      'width': 55,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'total':           {'label': 'Total',         'type': 'entero',     'width': 35,  'order': 4,  'groupable': False, 'sortable': True,  'aggregate': 'suma'},
        'entregados':      {'label': 'Entregados',    'type': 'entero',     'width': 40,  'order': 5,  'groupable': False, 'sortable': True,  'aggregate': 'suma'},
        'fecha_creacion':  {'label': 'Creacion',      'type': 'fecha',      'width': 65,  'order': 6,  'groupable': False, 'sortable': True,  'aggregate': None},
        'fecha_entrega':   {'label': 'Entrega',       'type': 'fecha_hora', 'width': 75,  'order': 7,  'groupable': False, 'sortable': True,  'aggregate': None},
    },
    'contratos': {
        'nombre_empresa':  {'label': 'Empresa',       'type': 'texto',      'width': 115, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'tipo':            {'label': 'Tipo',          'type': 'texto',      'width': 50,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estatus':         {'label': 'Estatus',       'type': 'texto',      'width': 50,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'fecha_inicio':    {'label': 'Inicio',        'type': 'fecha',      'width': 60,  'order': 4,  'groupable': False, 'sortable': True,  'aggregate': None},
        'fecha_fin':       {'label': 'Fin',           'type': 'fecha',      'width': 60,  'order': 5,  'groupable': False, 'sortable': True,  'aggregate': None},
        'dias_restantes':  {'label': 'Dias',          'type': 'entero',     'width': 35,  'order': 6,  'groupable': False, 'sortable': True,  'aggregate': None},
        'monto_total':     {'label': 'Monto',         'type': 'moneda',     'width': 60,  'order': 7,  'groupable': False, 'sortable': True,  'aggregate': 'suma'},
    },
    'balance': {
        'nombre_patrocinador': {'label': 'Patrocinador', 'type': 'texto',   'width': 120, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'tipo_pago':       {'label': 'Tipo Pago',     'type': 'texto',      'width': 70,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'monto':           {'label': 'Monto',         'type': 'moneda',     'width': 75,  'order': 3,  'groupable': False, 'sortable': True,  'aggregate': 'suma'},
        'referencia':      {'label': 'Referencia',    'type': 'texto',      'width': 85,  'order': 4,  'groupable': False, 'sortable': True,  'aggregate': None},
        'fecha_pago':      {'label': 'Fecha Pago',    'type': 'fecha',      'width': 70,  'order': 5,  'groupable': False, 'sortable': True,  'aggregate': None},
    },
    'tareas': {
        'tarea':           {'label': 'Tarea',         'type': 'texto',      'width': 150, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado':          {'label': 'Estado',        'type': 'texto',      'width': 65,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'asignado':        {'label': 'Asignado a',    'type': 'texto',      'width': 80,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'fecha':           {'label': 'Fecha',         'type': 'fecha_hora', 'width': 75,  'order': 4,  'groupable': False, 'sortable': True,  'aggregate': None},
    },
    'patrocinadores': {
        'nombre_empresa':  {'label': 'Empresa',       'type': 'texto',      'width': 150, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'rif':             {'label': 'RIF',           'type': 'texto',      'width': 75,  'order': 2,  'groupable': False, 'sortable': True,  'aggregate': None},
        'telefono':        {'label': 'Telefono',      'type': 'texto',      'width': 75,  'order': 3,  'groupable': False, 'sortable': True,  'aggregate': None},
        'tipo_contrato':   {'label': 'Contrato',      'type': 'texto',      'width': 70,  'order': 4,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado':          {'label': 'Estado',        'type': 'texto',      'width': 55,  'order': 5,  'groupable': True,  'sortable': True,  'aggregate': None},
    },
    'usuarios': {
        'nombre':          {'label': 'Nombre',        'type': 'texto',      'width': 110, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'email':           {'label': 'Email',         'type': 'texto',      'width': 120, 'order': 2,  'groupable': False, 'sortable': True,  'aggregate': None},
        'rol':             {'label': 'Rol',           'type': 'texto',      'width': 70,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'depto':           {'label': 'Depto',         'type': 'texto',      'width': 70,  'order': 4,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado':          {'label': 'Estado',        'type': 'texto',      'width': 55,  'order': 5,  'groupable': True,  'sortable': True,  'aggregate': None},
    },
    'mantenimiento': {
        'recurso':         {'label': 'Recurso',       'type': 'texto',      'width': 110, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'estado':          {'label': 'Estado',        'type': 'texto',      'width': 65,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'ingreso':         {'label': 'Ingreso',       'type': 'fecha',      'width': 65,  'order': 3,  'groupable': False, 'sortable': True,  'aggregate': None},
        'diagnostico':     {'label': 'Diagnostico',   'type': 'texto_largo','width': 130, 'order': 4,  'groupable': False, 'sortable': False, 'aggregate': None},
        'dias_en_taller':  {'label': 'Dias',          'type': 'entero',     'width': 45,  'order': 5,  'groupable': False, 'sortable': True,  'aggregate': 'promedio'},
    },
    'reels': {
        'nombre':          {'label': 'Nombre',        'type': 'texto',      'width': 120, 'order': 1,  'groupable': True,  'sortable': True,  'aggregate': None},
        'patrocinador':    {'label': 'Patrocinador',  'type': 'texto',      'width': 100, 'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'videos':          {'label': 'Videos',        'type': 'entero',     'width': 50,  'order': 3,  'groupable': False, 'sortable': True,  'aggregate': 'suma'},
        'duracion_total':  {'label': 'Duracion',      'type': 'duracion',   'width': 80,  'order': 4,  'groupable': False, 'sortable': True,  'aggregate': None},
        'creado_en':       {'label': 'Creado',        'type': 'fecha_hora', 'width': 75,  'order': 5,  'groupable': False, 'sortable': True,  'aggregate': None},
    },
    'bitacora': {
        'id':              {'label': 'ID',            'type': 'entero',     'width': 30,  'order': 1,  'groupable': False, 'sortable': True,  'aggregate': None},
        'usuario':         {'label': 'Usuario',       'type': 'texto',      'width': 85,  'order': 2,  'groupable': True,  'sortable': True,  'aggregate': None},
        'accion':          {'label': 'Accion',        'type': 'texto',      'width': 65,  'order': 3,  'groupable': True,  'sortable': True,  'aggregate': None},
        'modulo':          {'label': 'Modulo',        'type': 'texto',      'width': 65,  'order': 4,  'groupable': True,  'sortable': True,  'aggregate': None},
        'detalle':         {'label': 'Detalle',       'type': 'texto_largo','width': 145, 'order': 5,  'groupable': False, 'sortable': False, 'aggregate': None},
        'fecha':           {'label': 'Fecha',         'type': 'fecha_hora', 'width': 75,  'order': 6,  'groupable': False, 'sortable': True,  'aggregate': None},
    },
}


# ---------------------------------------------------------------------------
# Columnas por defecto (las que aparecen si el usuario no selecciona nada)
# ---------------------------------------------------------------------------

COLUMNAS_DEFAULT = {
    'guiones':        ['nombre', 'game', 'pregame', 'fecha_ejecucion', 'estado', 'tiempo_total'],
    'inventario':     ['id', 'nombre', 'tipo_nombre', 'estado_nombre', 'fecha_compra'],
    'premios':        ['nombre', 'patrocinador', 'estado', 'total', 'entregados', 'fecha_creacion'],
    'contratos':      ['nombre_empresa', 'tipo', 'estatus', 'fecha_inicio', 'fecha_fin', 'dias_restantes', 'monto_total'],
    'balance':        ['nombre_patrocinador', 'tipo_pago', 'monto', 'referencia', 'fecha_pago'],
    'tareas':         ['tarea', 'estado', 'asignado', 'fecha'],
    'patrocinadores': ['nombre_empresa', 'rif', 'telefono', 'tipo_contrato'],
    'usuarios':       ['nombre', 'email', 'rol', 'depto', 'estado'],
    'mantenimiento':  ['recurso', 'estado', 'ingreso', 'diagnostico'],
    'reels':          ['nombre', 'patrocinador', 'videos', 'duracion_total'],
    'bitacora':       ['id', 'usuario', 'accion', 'modulo', 'detalle', 'fecha'],
}
