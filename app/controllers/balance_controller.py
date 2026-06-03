from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from datetime import datetime, date

from app.services.balance_service import BalanceService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad
from app.forms.balance_form import PagoForm

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io


class BalanceController:
    def __init__(self):
        self.service = BalanceService()

    def dashboard(self):
        repo = self.service.repo
        form = PagoForm()

        contratos_raw = repo.obtener_contratos_activos()
        todos_pagos = self.service.obtener_todos_pagos()
        total_pagado = repo.get_total_pagado_general()
        top_contratos = self.service.obtener_top_contratos()
        pagos_recientes = self.service.obtener_historial_pagos(5)

        contratos_procesados = []
        saldo_pendiente_general = 0.0

        for contrato in contratos_raw:
            id_c = contrato['id_contrato']
            monto_pagado_contrato = repo.get_total_pagado_by_contrato(id_c) or 0.0
            monto_total_contrato = float(contrato['monto_total']) if contrato['monto_total'] else 0.0
            calc_saldo_pendiente = monto_total_contrato - monto_pagado_contrato

            if calc_saldo_pendiente > 0:
                saldo_pendiente_general += calc_saldo_pendiente

            pagos_del_contrato = [p for p in todos_pagos if p.id_contrato == id_c]
            ultimo_pago = pagos_del_contrato[0] if pagos_del_contrato else None

            contratos_procesados.append({
                'id_contrato': id_c,
                'nombre_patrocinador': contrato.get('nombre_patrocinador', 'Sin patrocinador'),
                'monto_total': monto_total_contrato,
                'saldo_pendiente': calc_saldo_pendiente,
                'ultimo_pago_monto': float(ultimo_pago.monto) if ultimo_pago else None,
                'ultimo_pago_fecha': ultimo_pago.fecha_pago if ultimo_pago else None,
            })

        data = {
            'total_contratos': len(contratos_procesados),
            'total_pagado': total_pagado if total_pagado else 0.0,
            'saldo_pendiente': saldo_pendiente_general,
            'contratos_activos': len(contratos_procesados),
            'pagos_recientes': pagos_recientes,
            'todos_pagos': todos_pagos,
            'top_contratos': top_contratos,
            'contratos_activos_lista': contratos_procesados,
            'form': form,
            'now': datetime.now(),
        }

        return render_template('balance/dashboard.html', **data)

    def registrar_pago(self):
        if not current_user.tiene_permiso('balance.create'):
            flash('No tienes permiso para registrar pagos', 'danger')
            return redirect(url_for('balance.dashboard'))

        id_contrato = request.form.get('id_contrato')
        monto = request.form.get('monto')
        tipo_pago = request.form.get('tipo_pago')
        referencia = request.form.get('referencia')
        fecha_pago = request.form.get('fecha_pago')
        hora_pago = request.form.get('hora_pago')
        notas = request.form.get('Descripción')

        if not id_contrato or not monto or not tipo_pago:
            flash('Todos los campos obligatorios deben ser llenados', 'danger')
            return redirect(url_for('balance.dashboard'))

        try:
            monto = float(monto)
            if monto <= 0:
                flash('El monto debe ser mayor a cero', 'danger')
                return redirect(url_for('balance.dashboard'))
        except ValueError:
            flash('Monto inválido', 'danger')
            return redirect(url_for('balance.dashboard'))

        try:
            fecha_pago_dt = datetime.strptime(fecha_pago, '%Y-%m-%d').date()
            hora_pago_dt = datetime.strptime(hora_pago, '%H:%M').time()
        except (ValueError, TypeError):
            fecha_pago_dt = date.today()
            hora_pago_dt = datetime.now().time()

        datos_pago = {
            'id_contrato': int(id_contrato),
            'monto': monto,
            'tipo_pago': tipo_pago,
            'referencia': referencia,
            'fecha_pago': fecha_pago_dt,
            'hora_pago': hora_pago_dt,
            'Descripción': notas,
        }

        resultado = self.service.registrar_pago(datos_pago, current_user.id)

        if resultado['success']:
            registrar_actividad('create', 'pagos', 'Registrar pago',
                                f'Pago ${monto:.2f} registrado en contrato #{id_contrato}')
            flash(resultado['mensaje'], 'success')
        else:
            for error in resultado.get('errores', []):
                flash(error, 'danger')

        return redirect(url_for('balance.dashboard'))

    def editar_pago(self):
        if not current_user.tiene_permiso('balance.edit'):
            flash('No tienes permiso para editar pagos', 'danger')
            return redirect(url_for('balance.dashboard'))

        pago_id = request.form.get('pago_id')
        monto = request.form.get('monto')
        tipo_pago = request.form.get('tipo_pago')
        referencia = request.form.get('referencia')
        fecha_pago = request.form.get('fecha_pago')
        hora_pago = request.form.get('hora_pago')
        notas = request.form.get('Descripción')

        if not pago_id or not monto or not tipo_pago:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('balance.dashboard'))

        try:
            fecha_pago_dt = datetime.strptime(fecha_pago, '%Y-%m-%d').date()
            hora_pago_dt = datetime.strptime(hora_pago, '%H:%M').time()
        except (ValueError, TypeError):
            fecha_pago_dt = date.today()
            hora_pago_dt = datetime.now().time()

        datos = {
            'monto': float(monto),
            'tipo_pago': tipo_pago,
            'referencia': referencia,
            'fecha_pago': fecha_pago_dt,
            'hora_pago': hora_pago_dt,
            'Descripción': notas,
        }

        resultado = self.service.editar_pago(pago_id, datos)

        if resultado['success']:
            registrar_actividad('update', 'pagos', 'Editar pago',
                                f'Pago #{pago_id} editado')
            flash('Pago actualizado exitosamente', 'success')
        else:
            flash(f'Error: {resultado["error"]}', 'danger')

        return redirect(url_for('balance.dashboard'))

    def eliminar_pago(self, pago_id):
        if not current_user.tiene_permiso('balance.delete'):
            flash('No tienes permiso para eliminar pagos', 'danger')
            return redirect(url_for('balance.dashboard'))

        resultado = self.service.eliminar_pago(pago_id)

        if resultado['success']:
            registrar_actividad('delete', 'pagos', 'Eliminar pago',
                                f'Pago #{pago_id} eliminado')
            flash('Pago eliminado exitosamente', 'success')
        else:
            flash(f'Error: {resultado["error"]}', 'danger')

        return redirect(url_for('balance.dashboard'))

    def api_contrato(self, id_contrato):
        repo = self.service.repo
        contrato = repo.obtener_contrato_por_id(id_contrato)

        if not contrato:
            return jsonify({'error': 'Contrato no encontrado'}), 404

        total_pagado = repo.get_total_pagado_by_contrato(id_contrato) or 0.0
        saldo_pendiente = float(contrato['monto_total']) - total_pagado

        return jsonify({
            'id_contrato': contrato['id_contrato'],
            'nombre_patrocinador': contrato.get('nombre_patrocinador'),
            'monto_total': float(contrato['monto_total']),
            'total_pagado': total_pagado,
            'saldo_pendiente': saldo_pendiente,
        })

    def api_pago(self, id_pago):
        repo = self.service.repo
        pago = repo.obtener_pago_por_id(id_pago)

        if not pago:
            return jsonify({'error': 'Pago no encontrado'}), 404

        contrato = repo.obtener_contrato_por_id(pago.id_contrato)

        return jsonify({
            'id_pago': pago.id_pago,
            'id_contrato': pago.id_contrato,
            'nombre_patrocinador': contrato['nombre_patrocinador'] if contrato else None,
            'monto': float(pago.monto),
            'tipo_pago': pago.tipo_pago,
            'referencia': pago.referencia,
            'fecha_pago': pago.fecha_pago.strftime('%d/%m/%Y') if pago.fecha_pago else '',
            'hora_pago': (datetime.min + pago.hora_pago).strftime('%H:%M') if pago.hora_pago else '',
            'Descripción': pago.Descripción,
        })

    def generar_pdf_contrato(self, contrato_id):
        repo = self.service.repo

        contrato_data = repo.obtener_contrato_por_id(contrato_id)
        if not contrato_data:
            flash('El contrato especificado no existe.', 'danger')
            return redirect(url_for('balance.dashboard'))

        monto_pagado_contrato = repo.get_total_pagado_by_contrato(contrato_id) or 0.0
        monto_total_contrato = float(contrato_data['monto_total']) if contrato_data['monto_total'] else 0.0
        saldo_pendiente_contrato = monto_total_contrato - monto_pagado_contrato

        todos_pagos = self.service.obtener_todos_pagos()
        pagos_contrato = [p for p in todos_pagos if p.id_contrato == contrato_id]

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        )

        story = []
        styles = getSampleStyleSheet()

        style_titulo = ParagraphStyle(
            'TituloReporte',
            parent=styles['Heading1'],
            fontSize=20, leading=24,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=6,
        )
        style_normal = styles['Normal']
        style_bold = ParagraphStyle(
            'TextoNegrita', parent=style_normal, fontName='Helvetica-Bold'
        )

        usuario_operador = getattr(current_user, 'nombre', 'Sistema')
        rol_usuario = getattr(current_user, 'rol', 'Administrador')
        depto_usuario = getattr(current_user, 'departamento', 'Operaciones')

        story.append(Paragraph("<b>ESTADIO ANTONIO HERRERA GUTIÉRREZ</b>", style_bold))
        story.append(Paragraph(f"Departamento: {depto_usuario} | Rol: {rol_usuario}", style_normal))
        story.append(Paragraph(f"<b>Generado por:</b> {usuario_operador.upper()}", style_normal))
        story.append(Paragraph(f"<b>Fecha de Emisión:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", style_normal))
        story.append(Spacer(1, 15))

        story.append(Paragraph(f"ESTADO DE CUENTA - CONTRATO #{contrato_id}", style_titulo))
        story.append(Spacer(1, 10))

        datos_patrocinador = [
            [Paragraph("<b>Patrocinador:</b>", style_normal),
             Paragraph(contrato_data.get('nombre_patrocinador', 'Sin nombre'), style_normal)],
            [Paragraph("<b>Monto Total Contratado:</b>", style_normal),
             Paragraph(f"${monto_total_contrato:,.2f}", style_normal)],
            [Paragraph("<b>Total Pagado a la Fecha:</b>", style_normal),
             Paragraph(f"${monto_pagado_contrato:,.2f}", style_normal)],
            [Paragraph("<b>Saldo Pendiente Neto:</b>", style_normal),
             Paragraph(f"<font color='red'><b>${saldo_pendiente_contrato:,.2f}</b></font>", style_normal)],
        ]

        tabla_info = Table(datos_patrocinador, colWidths=[150, 380])
        tabla_info.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(tabla_info)
        story.append(Spacer(1, 25))

        story.append(Paragraph("<b>Desglose de Transacciones Registradas</b>", styles['Heading3']))
        story.append(Spacer(1, 8))

        tabla_pagos_data = [[
            Paragraph("<b>ID Pago</b>", style_bold),
            Paragraph("<b>Fecha</b>", style_bold),
            Paragraph("<b>Tipo de Pago</b>", style_bold),
            Paragraph("<b>Referencia</b>", style_bold),
            Paragraph("<b>Monto</b>", style_bold),
        ]]

        for p in pagos_contrato:
            tabla_pagos_data.append([
                Paragraph(str(p.id_pago), style_normal),
                Paragraph(p.fecha_pago.strftime('%d/%m/%Y') if p.fecha_pago else '-', style_normal),
                Paragraph(p.tipo_pago or '-', style_normal),
                Paragraph(p.referencia or '-', style_normal),
                Paragraph(f"${float(p.monto):,.2f}", style_normal),
            ])

        if len(pagos_contrato) == 0:
            tabla_pagos_data.append([
                Paragraph("No se registran movimientos de pago para este contrato.", style_normal),
                "", "", "", "",
            ])

        tabla_pagos = Table(tabla_pagos_data, colWidths=[60, 90, 120, 130, 130])
        estilo_tabla_pagos = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#273aaadd")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ]
        if len(pagos_contrato) == 0:
            estilo_tabla_pagos.append(('SPAN', (0, 1), (-1, 1)))

        tabla_pagos.setStyle(TableStyle(estilo_tabla_pagos))
        story.append(tabla_pagos)

        doc.build(story)
        buffer.seek(0)

        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = (
            f'attachment; filename=Estado_Cuenta_Contrato_{contrato_id}.pdf'
        )
        return response
