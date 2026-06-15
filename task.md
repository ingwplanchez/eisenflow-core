# Tareas de Implementación — EisenFlow Core

Lista de tareas por fases según el plan de acción aprobado.

---

## 🛠️ Fase 1: Infraestructura Base y Testing
- [ ] Crear paquete de pruebas `tests/` y su archivo `__init__.py`
- [ ] Implementar `tests/conftest.py` con las fixtures base (`client`, `tarea_q1` a `tarea_q4`, etc.)
- [ ] Implementar `tests/test_models.py` (UM-01 a UM-10)
- [ ] Implementar `tests/test_api.py` (IA-01 a IA-08)
- [ ] Implementar `tests/test_regresion.py` (RG-01 a RG-06)
- [ ] Instalar dependencias de testing (`pytest`, `pytest-asyncio`, `httpx`, `pytest-cov`) y verificar ejecución completa de pruebas
- [ ] Registrar cambios y subir a GitHub (`feat: infraestructura de pruebas base`)

---

## 🔧 Fase 2: Corregir Funcionalidad Rota y Conectar Formulario HTML
- [ ] Configurar soporte para plantillas Jinja2, formularios HTML (`python-multipart`) y archivos estáticos en `app/main.py`
- [ ] Modificar `GET /` en `app/main.py` para renderizar `index.html` con el contexto del tablero Kanban
- [ ] Crear endpoint `POST /crear-tarea` en `app/main.py` para procesar el formulario HTML y redirigir a `/`
- [ ] Implementar mecanismo seguro de autogeneración de ID para evitar duplicados en memoria
- [ ] Agregar endpoint `GET /api/health` como alternativa al check base original
- [ ] Corregir Bootstrap CDN y clases CSS menores en `app/templates/index.html`
- [ ] Agregar tests para la Fase 2 (F2-01 a F2-04)
- [ ] Verificar ejecución de pruebas y realizar prueba manual del formulario en el navegador
- [ ] Registrar cambios y subir a GitHub (`fix: conexion de formulario HTML y correcciones visuales`)

---

## 📝 Fase 3: CRUD Completo de Tareas (Tablero Dinámico)
- [ ] Implementar métodos de negocio en `models.py` (`mover_tarea`, `eliminar_tarea`, `buscar_tarea`)
- [ ] Crear endpoint `PUT /tarea/{tarea_id}/mover` para mover tareas entre columnas Kanban
- [ ] Crear endpoint `DELETE /tarea/{tarea_id}` para eliminar tareas
- [ ] Crear endpoint `GET /tarea/{tarea_id}` para obtener el detalle de una tarea por su ID
- [ ] Agregar tests para la Fase 3 (KN-01 a KN-04, DEL-01 a DEL-02, GET-01 a GET-02)
- [ ] Verificar ejecución de la suite de pruebas completa y validez de la cobertura de código
- [ ] Registrar cambios y subir a GitHub (`feat: endpoints para mover, eliminar y consultar tareas`)

---

## 🛡️ Fase 4: Manejo de Errores y CORS
- [ ] Configurar e instalar middleware CORS abierto a todos los orígenes
- [ ] Agregar middlewares / exception handlers globales en `app/main.py` para `RequestValidationError` y excepciones generales (`500 Internal Error`)
- [ ] Agregar tests para la Fase 4 (ER-01 a ER-03)
- [ ] Ejecutar suite final de pruebas con reporte de cobertura completa (`pytest-cov`)
- [ ] Registrar cambios y subir a GitHub (`feat: control de excepciones y configuracion CORS`)
