from flask import render_template, request, redirect, url_for, flash
from app.services.reels_service import ReelsService
from app.repositories.patrocinador_repository import PatrocinadorRepository
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad


class ReelsController:
    def __init__(self):
        self.service = ReelsService()
        self.patro_repo = PatrocinadorRepository()

    def _patrocinadores_select(self):
        return [(p.id_patrocinador, p.nombre_empresa) for p in self.patro_repo.consultar(activos=True)]

    def _parsear_duracion_minutos(self, texto):
        if not texto:
            return 0
        texto = str(texto).strip()
        if ',' in texto:
            partes = texto.split(',')
            minutos = int(partes[0]) if partes[0] else 0
            seg_str = (partes[1] or '').ljust(2, '0')[:2]
            return minutos + int(seg_str) / 60.0
        try:
            return float(texto)
        except ValueError:
            return 0

    def dashboard(self):
        reels = self.service.obtener_reels()
        return render_template('reels/dashboardreels.html', reels=reels)

    def crear(self):
        if request.method == 'POST':
            reel = self.service.crear_reel({
                'nombre': request.form.get('nombre'),
                'patrocinado': request.form.get('patrocinado'),
                'duracion_total': self._parsear_duracion_minutos(request.form.get('duracion_total')),
            })
            if reel:
                self._procesar_videos_json(reel.id, request.form.get('videos_json'))
                registrar_actividad('create', 'reels', 'Crear reel',
                                    f'Reel "{request.form.get("nombre")}" creado')
                flash(f'Reel "{reel.nombre}" creado exitosamente', 'success')
                return redirect(url_for('reels.dashboard'))
            for err in self.service.errores:
                flash(err, 'danger')
        return render_template('reels/agregar_reel.html', patrocinadores=self._patrocinadores_select())

    def ver(self, id):
        reel = self.service.obtener_reel(id)
        if not reel:
            flash('Reel no encontrado', 'danger')
            return redirect(url_for('reels.dashboard'))
        return render_template('reels/ver_reel.html', reel=reel)

    def editar(self, id):
        reel = self.service.obtener_reel(id)
        if not reel:
            flash('Reel no encontrado', 'danger')
            return redirect(url_for('reels.dashboard'))
        if request.method == 'POST':
            reel = self.service.editar_reel(id, {
                'nombre': request.form.get('nombre'),
                'patrocinado': request.form.get('patrocinado'),
                'duracion_total': self._parsear_duracion_minutos(request.form.get('duracion_total')),
            })
            if reel:
                self._procesar_videos_json(reel.id, request.form.get('videos_json'))
                registrar_actividad('update', 'reels', 'Editar reel',
                                    f'Reel "{request.form.get("nombre")}" editado')
                flash('Reel actualizado exitosamente', 'success')
                return redirect(url_for('reels.ver', id=id))
            for err in self.service.errores:
                flash(err, 'danger')
        import json
        videos_json = json.dumps([{
            'nombre': v.nombre,
            'duracion': v.duracion_segundos
        } for v in reel.videos])
        total_seg = int(round((reel.duracion_total or 0) * 60))
        mins = total_seg // 60
        segs = total_seg % 60
        reel_duracion_texto = f"{mins},{segs}" if segs else str(mins)
        return render_template('reels/editar_reel.html', reel=reel, videos_json=videos_json, patrocinadores=self._patrocinadores_select(), reel_duracion_texto=reel_duracion_texto)

    def _procesar_videos_json(self, reel_id, videos_json):
        import json as json_lib
        from app.repositories.reels_repository import VideoRepository
        if not videos_json:
            return
        try:
            videos_data = json_lib.loads(videos_json)
        except (json_lib.JSONDecodeError, TypeError):
            return
        video_repo = VideoRepository()
        for v in video_repo.consultar_por_reel(reel_id):
            video_repo.eliminar(v.id)
        for i, v_data in enumerate(videos_data):
            try:
                segundos = int(float(v_data.get('duracion', 0)))
            except (ValueError, TypeError):
                segundos = 0
            self.service.agregar_video(reel_id, {
                'nombre': v_data.get('nombre', ''),
                'duracion_segundos': segundos,
                'orden': i + 1,
            })

    def eliminar(self, id):
        if self.service.eliminar_reel(id):
            registrar_actividad('delete', 'reels', 'Eliminar reel',
                                f'Reel #{id} eliminado')
            flash('Reel eliminado exitosamente', 'success')
        else:
            for err in self.service.errores:
                flash(err, 'danger')
        return redirect(url_for('reels.dashboard'))

    def agregar_video(self, reel_id):
        if request.method == 'POST':
            video = self.service.agregar_video(reel_id, {
                'nombre': request.form.get('nombre'),
                'duracion_segundos': request.form.get('duracion_segundos', 0),
                'orden': request.form.get('orden'),
            })
            if video:
                flash(f'Video "{video.nombre}" agregado al reel', 'success')
            else:
                for err in self.service.errores:
                    flash(err, 'danger')
        return redirect(url_for('reels.ver', id=reel_id))

    def eliminar_video(self, reel_id, video_id):
        self.service.eliminar_video(video_id, reel_id)
        flash('Video eliminado del reel', 'success')
        return redirect(url_for('reels.ver', id=reel_id))
