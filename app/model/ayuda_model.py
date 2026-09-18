# app/model/ayuda_model.py
# Preguntas frecuentes del Centro de Ayuda (contenido estático, sin BD).


def obtener_preguntas_frecuentes():
    """Devuelve las categorías con sus preguntas frecuentes y respuestas."""
    return [
        {
            'categoria': 'General',
            'icono': 'fa-circle-info',
            'preguntas': [
                {
                    'pregunta': '¿Qué es Itinerario?',
                    'respuesta': 'Itinerario es el sistema web de gestión operativa del Estadio Antonio Herrera Gutiérrez (béisbol). Permite administrar guiones de shows en vivo, estado on-air, inventario, contratos, patrocinadores, premios, balance, tareas, mantenimiento, reels, usuarios, roles y permisos, bitácora y reportes PDF, además de incluir un asistente virtual integrado.',
                },
                {
                    'pregunta': '¿Cómo inicio sesión?',
                    'respuesta': 'Accede a la página de acceso del sistema y escribe tu correo y contraseña. Verifica que las mayúsculas y el teclado estén bien y resuelve el código captcha si aparece. Al iniciar sesión, el sistema registra tu sesión en la bitácora.',
                },
                {
                    'pregunta': '¿Olvidé mi contraseña?',
                    'respuesta': 'En la pantalla de acceso usa el enlace "¿Olvidaste tu contraseña?". El sistema enviará al correo registrado las instrucciones o el restablecimiento. Si no recibes el correo, contacta al administrador del sistema.',
                },
                {
                    'pregunta': '¿Cómo cierro sesión?',
                    'respuesta': 'Haz clic en tu nombre, en la parte inferior del menú lateral, y elige "Cerrar Sesión". Desde ese mismo menú puedes acceder a "Mi Perfil" para revisar o actualizar tus datos.',
                },
                {
                    'pregunta': '¿El sistema se puede usar desde el celular?',
                    'respuesta': 'Sí. Toda la interfaz es adaptable (responsive) y el módulo En Vivo está diseñado con el teléfono vertical como plataforma principal.',
                },
            ],
        },
        {
            'categoria': 'Usuarios, roles y permisos',
            'icono': 'fa-users',
            'preguntas': [
                {
                    'pregunta': '¿Cómo se crea un usuario?',
                    'respuesta': 'Ingresa al módulo Usuarios (requiere el permiso correspondiente) y usa el botón "Nuevo usuario". Completa el nombre, correo, contraseña y asigna un rol. El correo debe ser único dentro del sistema.',
                },
                {
                    'pregunta': '¿Qué son los roles y permisos?',
                    'respuesta': 'Cada usuario pertenece a un rol, y cada rol tiene un conjunto de permisos (ver, crear, editar, eliminar, etc.) por módulo. Los permisos definen qué acciones puede realizar cada persona dentro del sistema.',
                },
                {
                    'pregunta': '¿Cómo sé qué permisos tengo?',
                    'respuesta': 'En el módulo "Roles y Permisos" (disponible para administradores) puedes ver la asignación de permisos por rol. Si no tienes acceso, consulta directamente a un administrador del sistema.',
                },
                {
                    'pregunta': 'Mi sesión se cerró de pronto, ¿qué pasó?',
                    'respuesta': 'El sistema permite una sola sesión por usuario. Si iniciaste sesión desde otro dispositivo, la sesión anterior se cierra. Se registra esta actividad en la bitácora.',
                },
            ],
        },
        {
            'categoria': 'Guión y En Vivo',
            'icono': 'fa-scroll',
            'preguntas': [
                {
                    'pregunta': '¿Qué es un guión?',
                    'respuesta': 'Un guión ordena las actividades de un show en elementos secuenciales. Se crea desde el módulo Guión y puede previsualizarse, replicarse o publicarse antes de su uso en un show en vivo.',
                },
                {
                    'pregunta': '¿Cómo funciona el módulo En Vivo?',
                    'respuesta': 'Desde En Vivo se selecciona el guión del show y se opera en tiempo real. Los elementos avanzan en orden estricto: pendiente → en curso → completado. Solo un guión puede estar en vivo a la vez.',
                },
                {
                    'pregunta': '¿Cómo avanzo al siguiente elemento en vivo?',
                    'respuesta': 'Con doble toque en el teléfono (o doble clic en la computadora) sobre el elemento actual. El elemento pasa a completado y el siguiente pasa a en curso.',
                },
                {
                    'pregunta': '¿Cómo retrocedo un elemento en vivo?',
                    'respuesta': 'Usa el botón ↩ para mandar el elemento actual a pendiente cuando lo marcaste por error y aún debes ejecutarlo. Al retroceder se reactiva el elemento pendiente anterior si corresponde.',
                },
                {
                    'pregunta': '¿Quién puede operar el show en vivo?',
                    'respuesta': 'El operador requiere el permiso envivo.control. Los espectadores con permiso de solo vista pueden seguir el estado del show sin poder modificarlo.',
                },
                {
                    'pregunta': '¿Qué significa "Solo un guión puede estar en vivo"?',
                    'respuesta': 'El sistema garantiza que no haya dos shows transmitiéndose a la vez: al iniciar un guión en vivo, cualquier otro debe finalizarse primero.',
                },
            ],
        },
        {
            'categoria': 'Tareas y notificaciones',
            'icono': 'fa-tasks',
            'preguntas': [
                {
                    'pregunta': '¿Cómo se asigna una tarea?',
                    'respuesta': 'Desde el módulo Gestión de Tareas puedes crear una tarea y asignarla a varios empleados o a un departamento completo. Los asignados reciben una notificación automática.',
                },
                {
                    'pregunta': '¿Qué significan las notificaciones?',
                    'respuesta': 'La campana del encabezado muestra avisos en tiempo real. Los tipos actuales son tarea_asignada y tarea_completada. Al hacer clic en una notificación se marca como leída y te lleva a la sección correspondiente.',
                },
                {
                    'pregunta': '¿Cómo completo una tarea?',
                    'respuesta': 'Abre la tarea desde "Mis Tareas", realiza el trabajo y usa la acción completar. El creador de la tarea recibe una notificación de que fue completada.',
                },
            ],
        },
        {
            'categoria': 'Inventario y mantenimiento',
            'icono': 'fa-cubes',
            'preguntas': [
                {
                    'pregunta': '¿Cómo registro un recurso en el inventario?',
                    'respuesta': 'Desde el módulo Inventario puedes crear recursos nuevos, editarlos, eliminarlos y gestionar asignaciones. Las asignaciones permiten saber quién tiene cada recurso y su estado actual.',
                },
                {
                    'pregunta': '¿Cómo funciona el mantenimiento?',
                    'respuesta': 'En el módulo Mantenimiento se registran las fallas de los recursos, se agregan notas y se registran la reparación o la baja. Se mantiene un historial de cada intervención.',
                },
                {
                    'pregunta': '¿Cómo controlo la salida y devolución de un recurso?',
                    'respuesta': 'Usa las acciones de asignar y devolver recurso desde el módulo Inventario o desde la gestión de asignaciones. El sistema registra quién tiene el recurso y desde cuándo.',
                },
            ],
        },
        {
            'categoria': 'Patrocinadores y contratos',
            'icono': 'fa-file-contract',
            'preguntas': [
                {
                    'pregunta': '¿Cómo registro un patrocinador?',
                    'respuesta': 'En el módulo Patrocinantes se registra cada patrocinador del estadio con sus datos de contacto y referencia.',
                },
                {
                    'pregunta': '¿Cómo registro un contrato?',
                    'respuesta': 'En el módulo Contratos se registran los acuerdos con patrocinadores: partes, vigencia y montos asociados. Cada contrato queda vinculado a su patrocinador.',
                },
            ],
        },
        {
            'categoria': 'Balance y reportes',
            'icono': 'fa-chart-line',
            'preguntas': [
                {
                    'pregunta': '¿Qué es el Balance?',
                    'respuesta': 'El módulo Balance muestra el estado financiero de la operación con sus ingresos y egresos para el control del estadio.',
                },
                {
                    'pregunta': '¿Cómo genero un reporte PDF?',
                    'respuesta': 'Ingresa al módulo Reportes, elige el tipo de reporte, aplica los filtros (rango de fechas, entidad, categoría, entre otros) y haz clic en Generar. El PDF se guarda en el sistema y queda registrado en el historial de reportes.',
                },
                {
                    'pregunta': '¿Qué es la bitácora?',
                    'respuesta': 'La bitácora guarda la actividad de los usuarios y las sesiones del sistema. Es un registro auditable de quién hizo qué acción y cuándo.',
                },
            ],
        },
        {
            'categoria': 'Asistente virtual',
            'icono': 'fa-robot',
            'preguntas': [
                {
                    'pregunta': '¿Qué es Aurora?',
                    'respuesta': 'Aurora es el asistente virtual integrado del sistema (basado en reglas, sin IA externa). Está disponible en la burbuja flotante y responde dudas sobre los módulos, estados, conteos y guías de uso. No sustituye las validaciones del servidor.',
                },
                {
                    'pregunta': '¿Sobre qué puedo preguntarle a Aurora?',
                    'respuesta': 'Puedes preguntarle cómo se usa cada módulo, qué pasos seguir para una acción, el estado de tus tareas y otros datos del sistema que tenga autorizados.',
                },
            ],
        },
    ]