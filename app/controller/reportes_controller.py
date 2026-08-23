import os
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, request, jsonify, send_file
from flask_login import current_user
from app.helpers.decorators import verificar_acceso
from app.model.reportes_model import ReporteModel

bp = Blueprint('reportes', __name__, url_prefix='/reportes')

PERMISSION_MAP = {
    'reportes.dashboard': 'dashboard.view',
}

bp.before_request(verificar_acceso(PERMISSION_MAP))


MODULOS_DISPONIBLES = {
    'guiones': {'nombre': 'Guiones', 'icono': 'fa-scroll'},
    'inventario': {'nombre': 'Inventario', 'icono': 'fa-boxes'},
    'premios': {'nombre': 'Premios', 'icono': 'fa-gift'},
    'contratos': {'nombre': 'Contratos', 'icono': 'fa-file-contract'},
    'balance': {'nombre': 'Balance / Pagos', 'icono': 'fa-balance-scale'},
    'tareas': {'nombre': 'Tareas', 'icono': 'fa-tasks'},
    'patrocinadores': {'nombre': 'Patrocinadores', 'icono': 'fa-handshake'},
    'usuarios': {'nombre': 'Usuarios', 'icono': 'fa-users'},
    'mantenimiento': {'nombre': 'Mantenimiento', 'icono': 'fa-tools'},
    'reels': {'nombre': 'Reels', 'icono': 'fa-video'},
    'bitacora': {'nombre': 'Bitácora', 'icono': 'fa-history'},
}


TIPO_CONTRATO_MAP = {'1': 'Bronce', '2': 'Plata', '3': 'Oro'}


def _filtros_contratos(params):
    from app.model.contrato_model import ContratoModel
    from app.model.patrocinador_model import PatrocinadorModel
    
    tipo = params.get('tipo')
    
    patrocinadores = PatrocinadorModel().consultar()
    if tipo and tipo in TIPO_CONTRATO_MAP:
        contratos = ContratoModel().consultar()
        ids_con_tipo = {c['id_patrocinador'] for c in contratos if str(c.get('tipo', '')) == tipo}
        patrocinadores = [p for p in patrocinadores if p['id_patrocinador'] in ids_con_tipo]
    
    kpi_ranges = {'monto_min': 0, 'monto_max': 9999999}
    try:
        db = ContratoModel()._get_db()
        with db.cursor() as cur:
            cur.execute("SELECT MIN(monto_total), MAX(monto_total) FROM contrato WHERE estado = 1")
            row = cur.fetchone()
            if row and row[0]:
                kpi_ranges = {'monto_min': float(row[0]), 'monto_max': float(row[1])}
    except Exception:
        pass
    
    fecha_min = None
    fecha_max = None
    try:
        db = ContratoModel()._get_db()
        with db.cursor() as cur:
            cur.execute("SELECT MIN(fecha_inicio), MAX(fecha_fin) FROM contrato WHERE estado = 1")
            row = cur.fetchone()
            if row and row[0]:
                fecha_min = row[0].strftime('%Y-%m-%d') if hasattr(row[0], 'strftime') else str(row[0])[:10]
                fecha_max = row[1].strftime('%Y-%m-%d') if hasattr(row[1], 'strftime') else str(row[1])[:10]
    except Exception:
        pass
    
    return jsonify({
        'patrocinadores': [{'id': p['id_patrocinador'], 'nombre': p['nombre_empresa']} for p in patrocinadores],
        'tipos': [{'value': k, 'label': v} for k, v in TIPO_CONTRATO_MAP.items()],
        'estatus': ['Borrador', 'Vigente', 'Vencido'],
        'monto_min': kpi_ranges['monto_min'],
        'monto_max': kpi_ranges['monto_max'],
        'fecha_min': fecha_min or '',
        'fecha_max': fecha_max or '',
    })


def _filtros_guiones(params):
    ESTADOS = ['borrador', 'publicado', 'en_vivo', 'finalizado']
    return jsonify({
        'estados': [{'value': s, 'label': s.capitalize()} for s in ESTADOS],
    })


def _filtros_inventario(params):
    from app.model.inventario_model import InventarioModel
    try:
        model = InventarioModel()
        db = model._get_db()
        tipo_filter = params.get('tipo_nombre', '')
        with db.cursor() as cur:
            if tipo_filter:
                cur.execute("SELECT id FROM tipo_recurso WHERE nombre = %s", (tipo_filter,))
                row = cur.fetchone()
                tipo_id = row['id'] if row else None
            else:
                tipo_id = None
            cur.execute("""
                SELECT DISTINCT t.id, t.nombre
                FROM tipo_recurso t
                JOIN recursos r ON r.tipo_id = t.id
                WHERE r.eliminado = 0
                ORDER BY t.nombre
            """)
            tipos = [r['nombre'] for r in cur.fetchall()]
            if tipo_id:
                cur.execute("""
                    SELECT DISTINCT e.id, e.nombre
                    FROM estado_recurso e
                    JOIN recursos r ON r.estado_id = e.id
                    WHERE r.eliminado = 0 AND r.tipo_id = %s
                    ORDER BY e.nombre
                """, (tipo_id,))
            else:
                cur.execute("""
                    SELECT DISTINCT e.id, e.nombre
                    FROM estado_recurso e
                    JOIN recursos r ON r.estado_id = e.id
                    WHERE r.eliminado = 0
                    ORDER BY e.nombre
                """)
            estados = [r['nombre'] for r in cur.fetchall()]
            cur.execute("SELECT MIN(costo), MAX(costo) FROM recursos WHERE eliminado = 0")
            row = cur.fetchone()
            costo_min = float(row[0]) if row and row[0] is not None else 0
            costo_max = float(row[1]) if row and row[1] is not None else 999999
        return jsonify({'tipos': tipos, 'estados': estados, 'costo_min': costo_min, 'costo_max': costo_max})
    except Exception as e:
        print(f"[_filtros_inventario] Error: {e}")
        return jsonify({'tipos': [], 'estados': [], 'costo_min': 0, 'costo_max': 999999})


def _filtros_premios(params):
    from app.model.patrocinador_model import PatrocinadorModel
    patrocinadores = PatrocinadorModel().consultar()
    return jsonify({
        'patrocinadores': [{'id': p['id_patrocinador'], 'nombre': p['nombre_empresa']} for p in patrocinadores],
    })


def _filtros_balance(params):
    from app.model.balance_model import BalanceModel
    from app.model.patrocinador_model import PatrocinadorModel
    try:
        db = BalanceModel()._get_db()
        tipos = []
        with db.cursor() as cur:
            cur.execute("SELECT DISTINCT tipo_pago FROM pagos_contratos WHERE tipo_pago IS NOT NULL ORDER BY tipo_pago")
            tipos = [r['tipo_pago'] for r in cur.fetchall()]
        rangos = {'monto_min': 0, 'monto_max': 99999999}
        with db.cursor() as cur:
            cur.execute("SELECT MIN(monto), MAX(monto) FROM pagos_contratos")
            row = cur.fetchone()
            if row and row[0]:
                rangos = {'monto_min': float(row[0]), 'monto_max': float(row[1])}
        patrocinadores = PatrocinadorModel().consultar()
        return jsonify({
            'tipos_pago': tipos,
            'patrocinadores': [{'id': p['id_patrocinador'], 'nombre': p['nombre_empresa']} for p in patrocinadores],
            'monto_min': rangos['monto_min'],
            'monto_max': rangos['monto_max'],
        })
    except Exception:
        return jsonify({'tipos_pago': [], 'patrocinadores': [], 'monto_min': 0, 'monto_max': 99999999})


def _filtros_tareas(params):
    from app.model.auth_model import UsuarioModel
    usuarios = UsuarioModel().consultar()
    return jsonify({
        'usuarios': [{'id': u.id, 'nombre': u.nombre} for u in usuarios if hasattr(u, 'id')],
        'estados': ['Pendiente', 'En Progreso', 'Completada'],
    })


def _filtros_patrocinadores(params):
    return jsonify({
        'tipos_contrato': [{'value': '1', 'label': 'Vigente'}, {'value': '2', 'label': 'Vencido'}],
    })


def _filtros_usuarios(params):
    from app.model.auth_model import UsuarioModel
    try:
        db = UsuarioModel()._get_db()
        roles = []
        deptos = []
        with db.cursor() as cur:
            cur.execute("SELECT DISTINCT rol FROM usuarios WHERE rol IS NOT NULL ORDER BY rol")
            roles = [r['rol'] for r in cur.fetchall()]
            cur.execute("SELECT DISTINCT departamento FROM usuarios WHERE departamento IS NOT NULL ORDER BY departamento")
            deptos = [r['departamento'] for r in cur.fetchall()]
        return jsonify({'roles': roles, 'departamentos': deptos})
    except Exception:
        return jsonify({'roles': [], 'departamentos': []})


def _filtros_mantenimiento(params):
    from app.model.mantenimiento_model import RecursoModel, MantenimientoModel
    try:
        db = MantenimientoModel()._get_db()
        recursos = RecursoModel().consultar() if hasattr(RecursoModel(), 'consultar') else []
        estados = []
        with db.cursor() as cur:
            cur.execute("SELECT DISTINCT estado FROM mantenimiento WHERE estado IS NOT NULL ORDER BY estado")
            estados = [r['estado'] for r in cur.fetchall()]
        return jsonify({
            'estados': estados,
            'recursos': [{'id': r.get('id', r.get('id_recurso', '')), 'nombre': r.get('nombre', '')} for r in recursos] if recursos else [],
        })
    except Exception:
        return jsonify({'estados': [], 'recursos': []})


def _filtros_reels(params):
    from app.model.patrocinador_model import PatrocinadorModel
    patrocinadores = PatrocinadorModel().consultar()
    return jsonify({
        'patrocinadores': [{'id': p['id_patrocinador'], 'nombre': p['nombre_empresa']} for p in patrocinadores],
    })


def _filtros_bitacora(params):
    from app.model.bitacora_model import ActividadModel
    model = ActividadModel()
    return jsonify({
        'usuarios': model.obtener_usuarios_distintos(),
        'acciones': model.obtener_acciones_distintas(),
        'modulos': model.obtener_modulos_distintos(),
    })


FILTROS_HANDLERS = {
    'guiones': _filtros_guiones,
    'inventario': _filtros_inventario,
    'premios': _filtros_premios,
    'contratos': _filtros_contratos,
    'balance': _filtros_balance,
    'tareas': _filtros_tareas,
    'patrocinadores': _filtros_patrocinadores,
    'usuarios': _filtros_usuarios,
    'mantenimiento': _filtros_mantenimiento,
    'reels': _filtros_reels,
    'bitacora': _filtros_bitacora,
}


COLUMNAS_TECNICAS = {
    'status', 'Estatus', 'eliminado', 'password_hash', 'password',
    'modificado_en', 'hora_creacion', 'hora_pago',
    'id_patrocinador', 'id_tipo', 'id_estado', 'tipo_id', 'estado_id',
    'recurso_id', 'usuario_id', 'sesion_id', 'guion_id', 'fecha_id',
    'entregado_por', 'registrado_por', 'id_usuario_creador',
    'ip_address', 'user_agent',
}


def _parsear_fecha(fecha_str):
    if not fecha_str:
        return None
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.strptime(fecha_str, fmt)
        except ValueError:
            continue
    return None


def _formatear_tiempo(segundos):
    if not segundos or segundos <= 0:
        return '0m'
    h = int(segundos) // 3600
    m = (int(segundos) % 3600) // 60
    if h > 0:
        return f'{h}h {m}m' if m > 0 else f'{h}h'
    return f'{m}m'


def _filtrar_por_fecha(datos, campo_fecha, fecha_inicio, fecha_fin):
    if not fecha_inicio and not fecha_fin:
        return datos
    resultado = []
    fi = _parsear_fecha(fecha_inicio)
    ff = _parsear_fecha(fecha_fin)
    if ff:
        ff = ff + timedelta(days=1)
    for d in datos:
        val = d.get(campo_fecha)
        if not val:
            resultado.append(d)
            continue
        try:
            if hasattr(val, 'date'):
                fecha = val
            else:
                for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y'):
                    try:
                        fecha = datetime.strptime(str(val)[:10], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    resultado.append(d)
                    continue
            if fi and fecha < fi:
                continue
            if ff and fecha >= ff:
                continue
            resultado.append(d)
        except Exception:
            resultado.append(d)
    return resultado


CAMPOS_FECHA = {
    'guiones': 'creado_en', 'inventario': 'fecha_compra',
    'premios': 'fecha_creacion', 'contratos': 'fecha_inicio',
    'balance': 'fecha_pago', 'tareas': 'fecha_asignacion_tarea',
    'patrocinadores': 'fecha_registro', 'mantenimiento': 'fecha_ingreso',
    'reels': 'creado_en', 'bitacora': 'created_at',
}


def _encontrar_fecha_minima(datos, campo_fecha):
    minima = None
    for d in datos:
        val = d.get(campo_fecha)
        if not val:
            continue
        try:
            if hasattr(val, 'date'):
                fecha = val
            else:
                for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y'):
                    try:
                        fecha = datetime.strptime(str(val)[:10], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    continue
            if minima is None or fecha < minima:
                minima = fecha
        except Exception:
            continue
    return minima.strftime('%Y-%m-%d') if minima else None


def _ordenar_datos(datos, campo, direccion='asc'):
    if not campo or not datos:
        return datos
    reverse = direccion == 'desc'
    return sorted(datos, key=lambda d: str(d.get(campo, '')).lower(), reverse=reverse)


def _fmt_video_dur(segundos):
    seg = int(segundos or 0)
    m, s = divmod(seg, 60)
    return f"{m}m {s}s" if m > 0 else f"{s}s"


def _sanitizar_para_reporte(modulo, datos):
    """Limpia datos crudos de DB para consumo en reportes PDF y preview.

    - Elimina listas/dicts anidados (ej. videos, historial, usuario object)
    - Elimina columnas técnicas (status, password_hash, ids no resueltos)
    - Resuelve IDs a nombres donde hay helpers disponibles
    - Aplica formato legible a valores crudos (segundos, montos)
    """
    from decimal import Decimal
    from app.model.auth_model import UsuarioModel
    from app.model.patrocinador_model import PatrocinadorModel

    resumen_ids = {}
    if modulo in ('reels', 'premios'):
        pm = PatrocinadorModel()
        pats = pm.consultar()
        resumen_ids['patrocinador'] = {p['id_patrocinador']: p['nombre_empresa'] for p in pats}
    if modulo in ('bitacora', 'tareas', 'mantenimiento'):
        try:
            um = UsuarioModel()
            users = um.consultar()
            resumen_ids['usuario'] = {u['id']: u['nombre'] for u in users if hasattr(u, 'get') or hasattr(u, 'nombre')}
            resumen_ids['usuario'].update({u.id: u.nombre for u in users if hasattr(u, 'id') and not isinstance(u, dict)})
        except Exception:
            resumen_ids['usuario'] = {}

    resultado = []
    for d in datos:
        fila = {}
        for k, v in d.items():
            if k in COLUMNAS_TECNICAS:
                continue
            if isinstance(v, (list, dict)):
                continue
            if hasattr(v, 'strftime'):
                fila[k] = v.strftime('%d/%m/%Y %H:%M' if hasattr(v, 'hour') else '%d/%m/%Y')
            elif isinstance(v, Decimal):
                fila[k] = float(v)
            elif isinstance(v, (int, float, str, bool, type(None))):
                fila[k] = v
        if not fila.get('id') and d.get('id_contrato'):
            fila['id'] = d['id_contrato']
        if not fila.get('id') and d.get('id_patrocinador'):
            fila['id'] = d['id_patrocinador']
        if not fila.get('id') and d.get('id_tarea'):
            fila['id'] = d['id_tarea']
        resultado.append(fila)

    if modulo == 'reels':
        for i, original in enumerate(datos):
            raw_name = resumen_ids['patrocinador'].get(original.get('patrocinado'), '')
            if raw_name:
                resultado[i]['patrocinado'] = raw_name
            duracion_seg = float(original.get('duracion_total', 0) or 0)
            minutos = int(duracion_seg // 60)
            segundos = int(duracion_seg % 60)
            resultado[i]['duracion'] = f"{minutos}m {segundos}s" if minutos > 0 else f"{segundos}s"

    if modulo == 'premios':
        for i, original in enumerate(datos):
            pid = original.get('id_patrocinador')
            if pid and 'patrocinador_nombre' not in original:
                resultado[i]['patrocinador_nombre'] = resumen_ids['patrocinador'].get(pid, '')
            if not original.get('estado'):
                resultado[i]['estado'] = 'entregado'
            if not original.get('fecha_creacion'):
                resultado[i]['fecha_creacion'] = original.get('fecha_entrega', '')

    if modulo == 'bitacora':
        for i, original in enumerate(datos):
            usuario_obj = original.get('usuario')
            if isinstance(usuario_obj, dict):
                resultado[i]['usuario_nombre'] = usuario_obj.get('nombre', '')
            elif hasattr(usuario_obj, 'nombre'):
                resultado[i]['usuario_nombre'] = usuario_obj.nombre
            if 'password_hash' in resultado[i]:
                del resultado[i]['password_hash']

    if modulo == 'mantenimiento':
        for i, original in enumerate(datos):
            recurso = original.get('recurso')
            if isinstance(recurso, dict):
                resultado[i]['recurso_nombre'] = recurso.get('nombre', '')
            if not resultado[i].get('recurso_nombre') and original.get('recurso_id'):
                resultado[i]['recurso_nombre'] = resumen_ids.get('recurso', {}).get(original['recurso_id'], '')

    return resultado


def _obtener_datos(modulo, filtros):
    from app.model.guion_model import GuionModel, ElementoGuionModel
    from app.model.inventario_model import InventarioModel
    from app.model.premio_model import PremioModel
    from app.model.contrato_model import ContratoModel
    from app.model.balance_model import BalanceModel
    from app.model.tarea_model import TareaModel, TareasAsignadasModel
    from app.model.patrocinador_model import PatrocinadorModel
    from app.model.auth_model import UsuarioModel
    from app.model.mantenimiento_model import RecursoModel, MantenimientoModel
    from app.model.reels_model import ReelModel
    from app.model.bitacora_model import ActividadModel

    fi = filtros.get('fecha_inicio', '')
    ff = filtros.get('fecha_fin', '')
    hoy = datetime.now().strftime('%Y-%m-%d')

    if fi and not ff:
        ff = hoy
    elif not fi and ff:
        fi = '2000-01-01'
    elif not fi and not ff and modulo in CAMPOS_FECHA:
        campo = CAMPOS_FECHA[modulo]
        model_map = {
            'guiones': lambda: GuionModel().consultar(),
            'inventario': lambda: InventarioModel().consultar(),
            'premios': lambda: PremioModel().obtener_premios_pendientes() + PremioModel().obtener_premios_entregados(),
            'contratos': lambda: ContratoModel().consultar(),
            'balance': lambda: BalanceModel().obtener_historial_pagos(limit=500),
            'tareas': lambda: TareaModel().consultar(),
            'patrocinadores': lambda: PatrocinadorModel().consultar(),
            'mantenimiento': lambda: MantenimientoModel().consultar(),
            'reels': lambda: ReelModel().consultar(),
            'bitacora': lambda: ActividadModel().consultar(limite=500),
        }
        loader = model_map.get(modulo)
        if loader:
            try:
                datos_carga = loader()
                minima = _encontrar_fecha_minima(datos_carga, campo)
                if minima:
                    fi = minima
                    ff = hoy
            except Exception:
                pass

    filtros['fecha_inicio'] = fi
    filtros['fecha_fin'] = ff

    if modulo == 'guiones':
        model = GuionModel()
        datos = model.consultar()
        if filtros.get('estado'):
            datos = [d for d in datos if d['estado'] == filtros['estado']]
        datos = _filtrar_por_fecha(datos, 'creado_en', fi, ff)
        elem_model = ElementoGuionModel()
        for d in datos:
            elems = elem_model.consultar(guion_id=d['id'])
            d['pregame'] = sum(1 for e in elems if e['tipo'] == 'pregame')
            d['game'] = sum(1 for e in elems if e['tipo'] == 'game')
            d['tiempo_segundos'] = sum(e.get('duracion_estimada', 0) or 0 for e in elems)
            fechas = model.obtener_fechas(d['id'])
            d['fecha_ejecucion'] = fechas[0]['fecha'].strftime('%d/%m/%Y') if fechas else '—'
            d['tiempo_total'] = _formatear_tiempo(d['tiempo_segundos'])
        borradores = sum(1 for d in datos if d.get('estado') == 'borrador')
        publicados = sum(1 for d in datos if d.get('estado') == 'publicado')
        en_vivo = sum(1 for d in datos if d.get('estado') == 'en_vivo')
        finalizados = sum(1 for d in datos if d.get('estado') == 'finalizado')
        tiempo_total_seg = sum(d.get('tiempo_segundos', 0) or 0 for d in datos)
        kpis = {
            'total': len(datos), 'borradores': borradores,
            'publicados': publicados, 'en_vivo': en_vivo,
            'finalizados': finalizados,
            'tiempo_total': _formatear_tiempo(tiempo_total_seg),
            'promedio_seg': round(tiempo_total_seg / len(datos)) if datos else 0,
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'inventario':
        model = InventarioModel()
        datos = model.consultar()
        if filtros.get('tipo_nombre'):
            datos = [d for d in datos if d.get('tipo_nombre') == filtros['tipo_nombre']]
        if filtros.get('estado_nombre'):
            datos = [d for d in datos if d.get('estado_nombre') == filtros['estado_nombre']]
        if filtros.get('costo_min'):
            try:
                min_v = float(filtros['costo_min'])
                datos = [d for d in datos if float(d.get('costo', 0) or 0) >= min_v]
            except ValueError:
                pass
        if filtros.get('costo_max'):
            try:
                max_v = float(filtros['costo_max'])
                datos = [d for d in datos if float(d.get('costo', 0) or 0) <= max_v]
            except ValueError:
                pass
        datos = _filtrar_por_fecha(datos, 'fecha_compra', fi, ff)
        tipos = {}
        estados = {}
        costo_total = 0
        for d in datos:
            tn = d.get('tipo_nombre', 'Otro')
            tipos[tn] = tipos.get(tn, 0) + 1
            en = d.get('estado_nombre', 'Desconocido')
            estados[en] = estados.get(en, 0) + 1
            costo_total += float(d.get('costo', 0) or 0)
        kpis = {
            'total': len(datos),
            'costo_total': round(costo_total, 2),
            'costo_promedio': round(costo_total / len(datos), 2) if datos else 0,
        }
        kpis['tipos'] = tipos
        kpis['estados'] = estados
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'premios':
        model = PremioModel()
        pendientes = model.obtener_premios_pendientes()
        entregados = model.obtener_premios_entregados()
        for p in pendientes:
            p['estado'] = 'pendiente'
        for p in entregados:
            p['estado'] = 'entregado'
        datos = pendientes + entregados
        if filtros.get('estado') == 'pendiente':
            datos = pendientes
        elif filtros.get('estado') == 'entregado':
            datos = entregados
        if filtros.get('patrocinador_id'):
            datos = [d for d in datos if str(d.get('id_patrocinador', '')) == str(filtros['patrocinador_id'])]
        datos = _filtrar_por_fecha(datos, 'fecha_creacion', fi, ff)
        pend_count = sum(1 for d in datos if d.get('estado') == 'pendiente')
        ent_count = sum(1 for d in datos if d.get('estado') == 'entregado')
        pat_counts = {}
        for d in datos:
            pn = d.get('patrocinador_nombre', 'Stock Libre')
            pat_counts[pn] = pat_counts.get(pn, 0) + 1
        kpis = {
            'total': len(datos), 'pendientes': pend_count,
            'entregados': ent_count,
            'tasa_entrega': f"{ent_count * 100 // len(datos)}%" if datos else "0%",
            'por_patrocinador': pat_counts,
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'contratos':
        model = ContratoModel()
        datos = model.consultar()

        if filtros.get('tipo'):
            datos = [d for d in datos if str(d.get('tipo', '')) == filtros['tipo']]
        if filtros.get('estatus'):
            datos = [d for d in datos if d.get('estatus') == filtros['estatus']]
        if filtros.get('patrocinador_id'):
            datos = [d for d in datos if str(d.get('id_patrocinador', '')) == str(filtros['patrocinador_id'])]
        if filtros.get('monto_min'):
            try:
                min_v = float(filtros['monto_min'])
                datos = [d for d in datos if float(d.get('monto_total', 0) or 0) >= min_v]
            except ValueError:
                pass
        if filtros.get('monto_max'):
            try:
                max_v = float(filtros['monto_max'])
                datos = [d for d in datos if float(d.get('monto_total', 0) or 0) <= max_v]
            except ValueError:
                pass

        datos = _filtrar_por_fecha(datos, 'fecha_inicio', fi, ff)

        for d in datos:
            d['tipo'] = TIPO_CONTRATO_MAP.get(str(d.get('tipo', '')), d.get('tipo', '—'))
            d['nombre_empresa'] = d.get('nombre_empresa', d.get('nombre_empresa', '—'))
            if d.get('fecha_fin'):
                try:
                    ffin = d['fecha_fin']
                    if hasattr(ffin, 'date'):
                        ffin = ffin.date() if hasattr(ffin, 'date') else ffin
                    dias = (ffin - date.today()).days if isinstance(ffin, date) else 0
                    d['dias_restantes'] = max(dias, 0)
                except Exception:
                    d['dias_restantes'] = '—'
            else:
                d['dias_restantes'] = '—'

        vigentes = sum(1 for d in datos if d.get('estatus') == 'Vigente')
        vencidos = sum(1 for d in datos if d.get('estatus') == 'Vencido')
        borradores = sum(1 for d in datos if d.get('estatus') == 'Borrador')
        monto_total = sum(float(d.get('monto_total', 0) or 0) for d in datos)
        montos = [float(d.get('monto_total', 0) or 0) for d in datos if d.get('monto_total')]
        monto_promedio = sum(montos) / len(montos) if montos else 0
        bronce = sum(1 for d in datos if d.get('tipo') == 'Bronce')
        plata = sum(1 for d in datos if d.get('tipo') == 'Plata')
        oro = sum(1 for d in datos if d.get('tipo') == 'Oro')

        patrocinador_montos = {}
        for d in datos:
            name = d.get('nombre_empresa', 'Desconocido')
            patrocinador_montos[name] = patrocinador_montos.get(name, 0) + float(d.get('monto_total', 0) or 0)
        top_pats = sorted(patrocinador_montos.items(), key=lambda x: x[1], reverse=True)[:5]

        monto_vigentes = sum(
            float(d.get('monto_total', 0) or 0)
            for d in datos if d.get('estatus') == 'Vigente'
        )
        vigentes_pct = f"{vigentes * 100 // len(datos)}%" if datos else "0%"

        kpis = {
            'total': len(datos),
            'vigentes': vigentes,
            'vencidos': vencidos,
            'borradores': borradores,
            'bronce': bronce,
            'plata': plata,
            'oro': oro,
            'monto_total': f"${monto_total:,.0f}",
            'monto_promedio': f"${monto_promedio:,.0f}",
            'monto_vigentes': f"${monto_vigentes:,.0f}",
            'monto_min': f"${min(montos):,.0f}" if montos else "$0",
            'monto_max': f"${max(montos):,.0f}" if montos else "$0",
            'vigentes_porcentaje': vigentes_pct,
            'top_patrocinadores': dict(top_pats),
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'balance':
        model = BalanceModel()
        pagos = model.obtener_historial_pagos(limit=500)
        datos = []
        for p in pagos:
            datos.append({
                'id_pago': p.id_pago,
                'id_contrato': p.id_contrato,
                'monto': float(p.monto) if p.monto else 0,
                'tipo_pago': p.tipo_pago or '',
                'referencia': p.referencia or '',
                'fecha_pago': str(p.fecha_pago)[:10] if p.fecha_pago else '',
                'hora_pago': str(p.hora_pago)[:5] if p.hora_pago else '',
                'descripcion': p.descripcion or '',
                'fecha_registro': str(p.fecha_registro)[:10] if p.fecha_registro else '',
                'nombre_patrocinador': p.nombre_patrocinador or 'Sin patrocinador',
            })
        if filtros.get('tipo_pago'):
            datos = [d for d in datos if d.get('tipo_pago') == filtros['tipo_pago']]
        if filtros.get('patrocinador_id'):
            datos = [d for d in datos if str(d.get('id_contrato', '')).startswith(str(filtros['patrocinador_id']))]
        if filtros.get('monto_min'):
            try: datos = [d for d in datos if d.get('monto', 0) >= float(filtros['monto_min'])]
            except ValueError: pass
        if filtros.get('monto_max'):
            try: datos = [d for d in datos if d.get('monto', 0) <= float(filtros['monto_max'])]
            except ValueError: pass
        datos = _filtrar_por_fecha(datos, 'fecha_pago', fi, ff)
        total = sum(d.get('monto', 0) for d in datos)
        tipos = {}
        for d in datos:
            t = d.get('tipo_pago', 'Otro')
            tipos[t] = tipos.get(t, 0) + 1
        montos_lista = [d.get('monto', 0) for d in datos]
        kpis = {
            'total_pagos': len(datos),
            'monto_total': f"${total:,.0f}",
            'promedio': f"${total / len(datos):,.0f}" if datos else "$0",
            'monto_min': f"${min(montos_lista):,.0f}" if montos_lista else "$0",
            'monto_max': f"${max(montos_lista):,.0f}" if montos_lista else "$0",
            'tipos_pago': tipos,
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'tareas':
        tarea_model = TareaModel()
        asign_model = TareasAsignadasModel()
        tareas = tarea_model.consultar()
        asignadas = asign_model.consultar()
        datos = []
        for t in tareas:
            t_id = t.get('id_tarea')
            row = {
                'id_tarea': t_id,
                'Nombre_Tarea': t.get('Nombre_Tarea', ''),
                'Instruccion': t.get('Instruccion', ''),
                'Estado': 'Pendiente',
                'asignado_a': '\u2014',
                'fecha_asignacion_tarea': '',
            }
            for a in asignadas:
                if a.get('id_tarea') == t_id:
                    row['Estado'] = a.get('Estado', 'Pendiente')
                    row['asignado_a'] = a.get('usuario_nombre', '\u2014')
                    row['fecha_asignacion_tarea'] = a.get('fecha_asignacion_tarea', '')
                    break
            datos.append(row)
        if filtros.get('Estado'):
            datos = [d for d in datos if d.get('Estado') == filtros['Estado']]
        if filtros.get('asignado_a'):
            datos = [d for d in datos if filtros['asignado_a'].lower() in d.get('asignado_a', '').lower()]
        datos = _filtrar_por_fecha(datos, 'fecha_asignacion_tarea', fi, ff)
        pendientes = sum(1 for d in datos if d.get('Estado') == 'Pendiente')
        en_progreso = sum(1 for d in datos if d.get('Estado') == 'En Progreso')
        completadas = sum(1 for d in datos if d.get('Estado') == 'Completada')
        completadas_pct = f"{completadas * 100 // len(datos)}%" if datos else "0%"
        kpis = {
            'total': len(datos), 'pendientes': pendientes,
            'en_progreso': en_progreso, 'completadas': completadas,
            'completadas_pct': completadas_pct,
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'patrocinadores':
        model = PatrocinadorModel()
        datos = model.consultar()
        tipo_map = {'1': 'Vigente', '2': 'Vencido'}
        for d in datos:
            d['tipo_contrato'] = tipo_map.get(str(d.get('tipo_contrato', '')), '—')
        if filtros.get('tipo_contrato'):
            datos = [d for d in datos if d.get('tipo_contrato') == filtros['tipo_contrato']]
        if filtros.get('estado_filter'):
            estado_val = int(filtros['estado_filter']) if filtros['estado_filter'].isdigit() else None
            if estado_val is not None:
                datos = [d for d in datos if d.get('estado') == estado_val]
        activos = sum(1 for d in datos if d.get('estado') == 1)
        inactivos = len(datos) - activos
        tipo_counts = {}
        for d in datos: tipo_counts[d.get('tipo_contrato', '—')] = tipo_counts.get(d.get('tipo_contrato', '—'), 0) + 1
        kpis = {'total': len(datos), 'activos': activos, 'inactivos': inactivos, 'por_tipo': tipo_counts}
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'usuarios':
        from app.model.usuario_model import UsuarioModel as UModel
        model = UModel()
        datos = model.consultar()
        if filtros.get('rol'):
            datos = [d for d in datos if d.get('rol') == filtros['rol']]
        if filtros.get('departamento'):
            datos = [d for d in datos if d.get('departamento') == filtros['departamento']]
        if filtros.get('activo'):
            is_active = filtros['activo'] in ('1', 'true', 'True')
            datos = [d for d in datos if bool(d.get('activo')) == is_active]
        datos = _filtrar_por_fecha(datos, 'fecha_registro', fi, ff)
        activos = sum(1 for d in datos if d.get('activo'))
        inactivos = sum(1 for d in datos if not d.get('activo'))
        roles = {}
        for d in datos:
            r = d.get('rol', 'Sin rol')
            roles[r] = roles.get(r, 0) + 1
        deptos = {}
        for d in datos:
            dp = d.get('departamento', 'Sin depto')
            deptos[dp] = deptos.get(dp, 0) + 1
        kpis = {'total': len(datos), 'activos': activos, 'inactivos': inactivos, 'roles': roles, 'departamentos': deptos}
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'mantenimiento':
        model = MantenimientoModel()
        datos = model.consultar()
        if filtros.get('estado'):
            datos = [d for d in datos if d.get('estado') == filtros['estado']]
        if filtros.get('recurso_id'):
            datos = [d for d in datos if str(d.get('recurso_id', '')) == str(filtros['recurso_id'])]
        datos = _filtrar_por_fecha(datos, 'fecha_ingreso', fi, ff)
        en_espera = sum(1 for d in datos if d.get('estado') == 'en_espera')
        en_reparacion = sum(1 for d in datos if d.get('estado') == 'en_reparacion')
        reparados = sum(1 for d in datos if d.get('estado') == 'reparado')
        dados_baja = sum(1 for d in datos if d.get('estado') == 'baja')
        recursos_freq = {}
        for d in datos:
            r = d.get('recurso_nombre', 'Desconocido')
            recursos_freq[r] = recursos_freq.get(r, 0) + 1
        top_recursos = sorted(recursos_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        kpis = {
            'total': len(datos), 'en_espera': en_espera,
            'en_reparacion': en_reparacion, 'reparados': reparados,
            'dados_baja': dados_baja, 'top_recursos': dict(top_recursos),
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'reels':
        model = ReelModel()
        datos = model.consultar()
        if filtros.get('patrocinador_id'):
            datos = [d for d in datos if str(d.get('patrocinado', '')) == str(filtros['patrocinador_id'])]
        datos = _filtrar_por_fecha(datos, 'creado_en', fi, ff)
        total_videos = sum(len(r.get('videos', [])) for r in datos)
        duracion_total_seg = sum(float(r.get('duracion_total', 0) or 0) * 60 for r in datos)
        for d in datos:
            d['videos_count'] = len(d.get('videos', []))
            duracion_seg = float(d.get('duracion_total', 0) or 0) * 60
            minutos = int(duracion_seg // 60)
            segundos = int(duracion_seg % 60)
            d['duracion'] = f"{minutos}m {segundos}s" if minutos > 0 else f"{segundos}s"
            if hasattr(d.get('creado_en'), 'strftime'):
                d['creado_en'] = d['creado_en'].strftime('%d/%m/%Y %H:%M')
            videos = d.get('videos', [])
            d['videos_detalle'] = '\n'.join(
                f"{i+1}. {v.get('nombre', '')} ({_fmt_video_dur(v.get('duracion_segundos', 0))})"
                for i, v in enumerate(videos)
            ) if videos else 'Sin videos'
        duracion_total_min = duracion_total_seg / 60
        kpis = {
            'total': len(datos), 'total_videos': total_videos,
            'duracion_total': f"{duracion_total_min:.0f} min",
            'duracion_promedio': f"{duracion_total_min / len(datos):.0f} min" if datos else "0 min",
        }
        return datos, kpis

    elif modulo == 'bitacora':
        model = ActividadModel()
        consulta_filtros = {'limite': 500}
        if filtros.get('usuario_id'):
            consulta_filtros['usuario_id'] = filtros['usuario_id']
        if filtros.get('tipo_accion'):
            consulta_filtros['tipo_accion'] = filtros['tipo_accion']
        if filtros.get('modulo_filter'):
            consulta_filtros['modulo'] = filtros['modulo_filter']
        datos = model.consultar(**consulta_filtros)
        fi = filtros.get('fecha_inicio')
        ff = filtros.get('fecha_fin')
        datos = _filtrar_por_fecha(datos, 'created_at', fi, ff)
        creaciones = sum(1 for d in datos if d.get('tipo_accion') == 'create')
        ediciones = sum(1 for d in datos if d.get('tipo_accion') == 'update')
        eliminaciones = sum(1 for d in datos if d.get('tipo_accion') == 'delete')
        modulos = {}
        for d in datos:
            m = d.get('modulo', 'Otro')
            modulos[m] = modulos.get(m, 0) + 1
        usuarios = {}
        for d in datos:
            uo = d.get('usuario')
            nombre = 'Desconocido'
            if isinstance(uo, dict):
                nombre = uo.get('nombre', 'Desconocido')
            elif hasattr(uo, 'nombre'):
                nombre = uo.nombre
            usuarios[nombre] = usuarios.get(nombre, 0) + 1
        top_usuarios = sorted(usuarios.items(), key=lambda x: x[1], reverse=True)[:5]
        kpis = {
            'total': len(datos),
            'creaciones': creaciones,
            'ediciones': ediciones,
            'eliminaciones': eliminaciones,
            'modulos': modulos,
            'top_usuarios': dict(top_usuarios),
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    elif modulo == 'resumen':
        from app.model.guion_model import GuionModel
        from app.model.inventario_model import InventarioModel
        from app.model.premio_model import PremioModel
        from app.model.contrato_model import ContratoModel
        from app.model.balance_model import BalanceModel
        from app.model.tarea_model import TareaModel
        from app.model.patrocinador_model import PatrocinadorModel
        from app.model.auth_model import UsuarioModel
        from app.model.mantenimiento_model import MantenimientoModel
        from app.model.reels_model import ReelModel
        modulos = [
            ('Guiones', GuionModel().consultar(), lambda d: d.get('estado') == 'publicado'),
            ('Inventario', InventarioModel().consultar(), lambda d: d.get('estado_nombre') == 'Disponible'),
            ('Premios', PremioModel().consultar(), lambda d: d.get('estado') == 'entregado'),
            ('Contratos', ContratoModel().consultar(), lambda d: d.get('estatus') == 'Vigente'),
            ('Tareas', TareaModel().consultar(), lambda d: d.get('Estado') == 'Completada'),
            ('Patrocinadores', PatrocinadorModel().consultar(), lambda d: d.get('estado') == 1),
            ('Usuarios', UsuarioModel().consultar(), lambda d: d.get('activo')),
            ('Mantenimiento', MantenimientoModel().consultar(), lambda d: d.get('estado') in ('reparado',)),
            ('Reels', ReelModel().consultar(), lambda d: True),
        ]
        datos = [{
            'modulo': n, 'total': len(d),
            'activos': sum(1 for x in d if f(x)),
            'inactivos': sum(1 for x in d if not f(x)),
        } for n, d, f in modulos]
        total_reg = sum(d.get('total', 0) for d in datos)
        total_act = sum(d.get('activos', 0) for d in datos)
        kpis = {
            'modulos': len(datos),
            'total_registros': total_reg,
            'total_activos': total_act,
            'total_inactivos': total_reg - total_act,
        }
        datos = _sanitizar_para_reporte(modulo, datos)
        return datos, kpis

    return [], {}


COLUMNAS_PREVIEW = {
    'guiones': [
        {'key': 'nombre', 'label': 'Nombre'},
        {'key': 'game', 'label': 'Game'},
        {'key': 'pregame', 'label': 'Pre-Game'},
        {'key': 'fecha_ejecucion', 'label': 'Ejecución'},
        {'key': 'estado', 'label': 'Estado'},
        {'key': 'tiempo_total', 'label': 'Tiempo'},
    ],
    'inventario': [
        {'key': 'id', 'label': 'ID'},
        {'key': 'nombre', 'label': 'Nombre'},
        {'key': 'tipo_nombre', 'label': 'Tipo'},
        {'key': 'estado_nombre', 'label': 'Estado'},
        {'key': 'costo', 'label': 'Costo'},
        {'key': 'fecha_compra', 'label': 'Fecha Compra'},
    ],
    'patrocinadores': [
        {'key': 'nombre_empresa', 'label': 'Empresa'},
        {'key': 'rif', 'label': 'RIF'},
        {'key': 'telefono', 'label': 'Teléfono'},
        {'key': 'tipo_contrato', 'label': 'Contrato'},
        {'key': 'estado', 'label': 'Activo'},
    ],
    'contratos': [
        {'key': 'nombre_empresa', 'label': 'Patrocinador'},
        {'key': 'tipo', 'label': 'Tipo'},
        {'key': 'estatus', 'label': 'Estatus'},
        {'key': 'monto_total', 'label': 'Monto'},
        {'key': 'fecha_inicio', 'label': 'Inicio'},
        {'key': 'fecha_fin', 'label': 'Fin'},
        {'key': 'dias_restantes', 'label': 'Días Restantes'},
    ],
    'balance': [
        {'key': 'nombre_patrocinador', 'label': 'Patrocinador'},
        {'key': 'tipo_pago', 'label': 'Tipo Pago'},
        {'key': 'monto', 'label': 'Monto'},
        {'key': 'referencia', 'label': 'Referencia'},
        {'key': 'fecha_pago', 'label': 'Fecha Pago'},
    ],
    'premios': [
        {'key': 'nombre', 'label': 'Nombre'},
        {'key': 'patrocinador_nombre', 'label': 'Patrocinador'},
        {'key': 'estado', 'label': 'Estado'},
        {'key': 'cantidad', 'label': 'Total'},
        {'key': 'cantidad_entregada', 'label': 'Entregados'},
        {'key': 'fecha_creacion', 'label': 'Creación'},
    ],
    'tareas': [
        {'key': 'Nombre_Tarea', 'label': 'Tarea'},
        {'key': 'Estado', 'label': 'Estado'},
        {'key': 'asignado_a', 'label': 'Asignado a'},
        {'key': 'fecha_asignacion_tarea', 'label': 'Fecha'},
    ],
    'usuarios': [
        {'key': 'nombre', 'label': 'Nombre'},
        {'key': 'email', 'label': 'Email'},
        {'key': 'rol', 'label': 'Rol'},
        {'key': 'departamento', 'label': 'Depto'},
        {'key': 'activo', 'label': 'Estado'},
    ],
    'mantenimiento': [
        {'key': 'recurso_nombre', 'label': 'Recurso'},
        {'key': 'estado', 'label': 'Estado'},
        {'key': 'fecha_ingreso', 'label': 'Ingreso'},
        {'key': 'diagnostico', 'label': 'Diagnóstico'},
    ],
    'reels': [
        {'key': 'nombre', 'label': 'Nombre'},
        {'key': 'patrocinado', 'label': 'Patrocinador'},
        {'key': 'videos_count', 'label': 'Videos'},
        {'key': 'duracion', 'label': 'Duración'},
        {'key': 'creado_en', 'label': 'Creado'},
    ],
    'bitacora': [
        {'key': 'usuario_nombre', 'label': 'Usuario'},
        {'key': 'tipo_accion', 'label': 'Acción'},
        {'key': 'modulo', 'label': 'Módulo'},
        {'key': 'detalle', 'label': 'Detalle'},
        {'key': 'created_at', 'label': 'Fecha'},
    ],
    'resumen': [
        {'key': 'modulo', 'label': 'Módulo'},
        {'key': 'total', 'label': 'Total'},
        {'key': 'activos', 'label': 'Activos'},
        {'key': 'inactivos', 'label': 'Inactivos'},
    ],
}


def _serializar_datos(datos):
    """Convierte datos planos a JSON-safe. Ya vienen sanitizados."""
    from decimal import Decimal
    resultado = []
    for d in datos:
        fila = {}
        for k, v in d.items():
            if isinstance(v, datetime):
                fila[k] = v.strftime('%d/%m/%Y %H:%M' if hasattr(v, 'hour') else '%d/%m/%Y')
            elif isinstance(v, Decimal):
                fila[k] = float(v)
            elif isinstance(v, (int, float, str, bool, type(None))):
                fila[k] = v
        resultado.append(fila)
    return resultado


@bp.route('/filtros/<modulo>', methods=['GET'])
def filtros_modulo(modulo):
    handler = FILTROS_HANDLERS.get(modulo)
    if handler:
        return handler(request.args)
    return jsonify({'error': 'Módulo no soportado'}), 400


@bp.route('/', methods=['GET'])
def dashboard():
    reportes = ReporteModel().listar(limite=50)
    return render_template('reportes/dashboard.html',
                           modulos=MODULOS_DISPONIBLES,
                           reportes=reportes,
                           columnas_preview=COLUMNAS_PREVIEW)


@bp.route('/filtros-bitacora', methods=['GET'])
def filtros_bitacora():
    from app.model.bitacora_model import ActividadModel
    model = ActividadModel()
    return jsonify({
        'usuarios': model.obtener_usuarios_distintos(),
        'acciones': model.obtener_acciones_distintas(),
        'modulos': model.obtener_modulos_distintos(),
    })


@bp.route('/preview', methods=['POST'])
def preview():
    modulo = request.form.get('modulo', '')
    if modulo not in MODULOS_DISPONIBLES:
        return jsonify({'error': 'Módulo no válido'}), 400
    try:
        filtros = {}
        for key in request.form:
            if key in ('modulo', 'csrf_token', 'sort_by', 'sort_dir'):
                continue
            val = request.form.get(key)
            if val:
                filtros[key] = val

        sort_by = request.form.get('sort_by', '')
        sort_dir = request.form.get('sort_dir', 'asc')

        datos, kpis = _obtener_datos(modulo, filtros)
        datos = _ordenar_datos(datos, sort_by, sort_dir)
        cols = COLUMNAS_PREVIEW.get(modulo)
        if cols:
            col_keys = [c['key'] for c in cols]
            datos = [{k: d.get(k) for k in col_keys} for d in datos]
        datos_serializados = _serializar_datos(datos)

        kpis_display = {}
        for k, v in kpis.items():
            if isinstance(v, (dict, list)):
                continue
            kpis_display[k] = v

        resp = {
            'datos': datos_serializados[:100],
            'total': len(datos),
            'kpis': kpis_display,
            'modulo': MODULOS_DISPONIBLES[modulo]['nombre'],
        }
        if cols:
            resp['columnas'] = cols
        return jsonify(resp)
    except Exception as e:
        return jsonify({'error': f'Error al cargar datos: {str(e)}'}), 500


@bp.route('/generar', methods=['POST'])
def generar():
    modulo = request.form.get('modulo', '')
    if modulo not in MODULOS_DISPONIBLES:
        return jsonify({'error': 'Módulo no válido'}), 400
    try:
        filtros = {}
        for key in request.form:
            if key in ('modulo', 'csrf_token', 'sort_by', 'sort_dir'):
                continue
            val = request.form.get(key)
            if val:
                filtros[key] = val

        sort_by = request.form.get('sort_by', '')
        sort_dir = request.form.get('sort_dir', 'asc')

        datos, kpis = _obtener_datos(modulo, filtros)
        if not datos:
            return jsonify({'error': 'No hay datos para los filtros seleccionados'}), 400

        datos = _ordenar_datos(datos, sort_by, sort_dir)
        if sort_by:
            label = sort_by
            cols = COLUMNAS_PREVIEW.get(modulo, [])
            for c in cols:
                if c['key'] == sort_by:
                    label = c['label']
                    break
            dir_label = 'Descendente' if sort_dir == 'desc' else 'Ascendente'
            filtros['orden'] = f"{label} ({dir_label})"

        generadores = {
            'guiones': lambda: __import__('app.helpers.generators.guiones_report', fromlist=['GuionesReport']).GuionesReport(current_user),
            'inventario': lambda: __import__('app.helpers.generators.inventario_report', fromlist=['InventarioReport']).InventarioReport(current_user),
            'premios': lambda: __import__('app.helpers.generators.premios_report', fromlist=['PremiosReport']).PremiosReport(current_user),
            'contratos': lambda: __import__('app.helpers.generators.contratos_report', fromlist=['ContratosReport']).ContratosReport(current_user),
            'balance': lambda: __import__('app.helpers.generators.balance_report', fromlist=['BalanceReport']).BalanceReport(current_user),
            'tareas': lambda: __import__('app.helpers.generators.tareas_report', fromlist=['TareasReport']).TareasReport(current_user),
            'patrocinadores': lambda: __import__('app.helpers.generators.patrocinadores_report', fromlist=['PatrocinadoresReport']).PatrocinadoresReport(current_user),
            'usuarios': lambda: __import__('app.helpers.generators.usuarios_report', fromlist=['UsuariosReport']).UsuariosReport(current_user),
            'mantenimiento': lambda: __import__('app.helpers.generators.mantenimiento_report', fromlist=['MantenimientoReport']).MantenimientoReport(current_user),
            'reels': lambda: __import__('app.helpers.generators.reels_report', fromlist=['ReelsReport']).ReelsReport(current_user),
            'bitacora': lambda: __import__('app.helpers.generators.bitacora_report', fromlist=['BitacoraReport']).BitacoraReport(current_user),
            'resumen': lambda: __import__('app.helpers.generators.resumen_report', fromlist=['ResumenReport']).ResumenReport(current_user),
        }

        if modulo not in generadores:
            return jsonify({'error': 'Generador no disponible'}), 400

        generador = generadores[modulo]()
        pdf_bytes = generador.generate(datos, filtros=filtros, kpis=kpis)
        ruta, nombre = generador.save(pdf_bytes, current_user.id, filtros)

        return jsonify({
            'mensaje': 'Reporte generado exitosamente',
            'descargar': f'/reportes/descargar/{nombre}',
        })
    except Exception as e:
        return jsonify({'error': f'Error al generar reporte: {str(e)}'}), 500


@bp.route('/descargar/<nombre>', methods=['GET'])
def descargar(nombre):
    reportes = ReporteModel().listar()
    reporte = next((r for r in reportes if r['archivo_ruta'].endswith(nombre)), None)
    if not reporte:
        return jsonify({'error': 'Reporte no encontrado'}), 404

    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'reportes')
    filepath = os.path.join(base_dir, reporte['archivo_ruta'])
    if not os.path.exists(filepath):
        return jsonify({'error': 'Archivo no encontrado'}), 404

    return send_file(filepath, as_attachment=True, download_name=reporte['archivo_nombre'])


@bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    ok = ReporteModel().eliminar(id)
    if ok:
        return jsonify({'mensaje': 'Reporte eliminado exitosamente'})
    return jsonify({'error': 'Error al eliminar reporte'}), 400
