# AGENTS.md — EisenFlow Core

> Guía para agentes de IA y colaboradores que trabajen en este proyecto.
> Última actualización: 2026-06-10

---

## 📌 Descripción General del Proyecto

**EisenFlow Core** es un microservicio de productividad construido con **FastAPI** (Python 3.10+).
Implementa dos conceptos clave:

1. **Matriz de Eisenhower** — Clasifica tareas automáticamente en 4 cuadrantes según urgencia e importancia:
   - **Q1 – Hacer**: Urgente + Importante
   - **Q2 – Programar**: No Urgente + Importante
   - **Q3 – Delegar**: Urgente + No Importante
   - **Q4 – Eliminar**: No Urgente + No Importante

2. **Tablero Kanban** — Organiza las tareas clasificadas en 3 columnas:
   - `To Do` → `In Progress` → `Done`

El sistema opera actualmente **en memoria** (sin persistencia a disco/base de datos).

---

## 🏗️ Arquitectura y Estructura del Proyecto

```text
eisenflow-core/
├── app/
│   ├── __init__.py          # Paquete Python (vacío)
│   ├── main.py              # Punto de entrada FastAPI, definición de rutas
│   ├── models.py            # Modelos Pydantic (Tarea) y lógica de negocio (MatrizEisenhower)
│   ├── templates/
│   │   └── index.html       # Dashboard Kanban con Jinja2 + Bootstrap 5
│   └── static/
│       └── css/             # Directorio para archivos CSS (actualmente vacío)
├── .venv/                   # Entorno virtual Python (NO modificar, NO commitear)
├── requirements.txt         # Dependencias del proyecto (generado con pip freeze)
├── notas.txt                # Notas de desarrollo del autor
└── README.md                # Documentación del proyecto
```

### Archivos Clave

| Archivo | Responsabilidad |
|---------|----------------|
| [`main.py`](file:///c:/Users/USER/Documents/wplanchez/Portafolio/Repositorios/FastAPI/eisenflow-core/app/main.py) | Instancia de `FastAPI`, rutas de la API (`GET /`, `POST /tarea/clasificar`, `GET /tablero`) |
| [`models.py`](file:///c:/Users/USER/Documents/wplanchez/Portafolio/Repositorios/FastAPI/eisenflow-core/app/models.py) | Modelo `Tarea` (Pydantic BaseModel), clase `MatrizEisenhower` con lógica de clasificación y estado Kanban |
| [`index.html`](file:///c:/Users/USER/Documents/wplanchez/Portafolio/Repositorios/FastAPI/eisenflow-core/app/templates/index.html) | Dashboard HTML con formulario de captura y visualización del tablero Kanban |

---

## 🔌 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje base |
| FastAPI | 0.136.x | Framework web asíncrono |
| Pydantic | 2.13.x | Validación de datos y esquemas |
| Uvicorn | 0.49.x | Servidor ASGI |
| Jinja2 | 3.1.x | Motor de plantillas HTML |
| Bootstrap | 5.3.0 (CDN) | Framework CSS para la UI |
| python-multipart | 0.0.32 | Procesamiento de formularios HTML |
| Requests | 2.34.x | Cliente HTTP (preparado para integración con n8n) |

---

## 📡 API Endpoints Existentes

| Método | Ruta | Descripción | Request Body | Response |
|--------|------|-------------|-------------|----------|
| `GET` | `/` | Health check | — | `{"message": "EisenFlow API is running..."}` |
| `POST` | `/tarea/clasificar` | Crea y clasifica una tarea | `Tarea` (JSON) | `Tarea` con cuadrante asignado |
| `GET` | `/tablero` | Retorna el tablero Kanban completo | — | `Dict[str, List[Tarea]]` |

### Modelo `Tarea`

```python
class Tarea(BaseModel):
    id: int              # Identificador único
    titulo: str          # Descripción de la tarea
    urgente: bool        # ¿Es urgente?
    importante: bool     # ¿Es importante?
    estado: str = "To Do"  # Estado Kanban (To Do | In Progress | Done)
    cuadrante: str = ""    # Cuadrante Eisenhower asignado automáticamente
```

---

## 📜 Convenciones y Reglas para Agentes

### Código

1. **Idioma del código**: Los nombres de variables, clases, funciones y campos están en **español** (ej. `Tarea`, `titulo`, `urgente`, `clasificar_tarea`). Mantener esta convención.
2. **Idioma de comentarios y docstrings**: Español.
3. **Rutas de API**: Están en español con kebab-case (ej. `/tarea/clasificar`). Mantener el patrón.
4. **Tipo de funciones**: Todas las rutas de FastAPI usan `async def`. Mantener.
5. **Modelo Pydantic**: Usar `BaseModel` de Pydantic v2 para validación de entrada/salida.
6. **Sin ORM actual**: No hay base de datos ni ORM. El estado vive en memoria en la instancia de `MatrizEisenhower`.
7. **Formateo**: Seguir PEP 8. Indentación de 4 espacios.

### Archivos

1. **NO modificar**: `.venv/`, `__pycache__/`, archivos generados.
2. **NO commitear**: `.venv/`, `__pycache__/`, `*.pyc`.
3. **Actualizar `requirements.txt`**: Si se agrega una nueva dependencia, regenerar con `pip freeze > requirements.txt`.

### Arquitectura

1. **Separación de responsabilidades**:
   - `models.py` → Modelos de datos + lógica de negocio
   - `main.py` → Rutas HTTP y configuración de FastAPI
   - `templates/` → Interfaz visual (Jinja2)
   - `static/` → Archivos estáticos (CSS, JS, imágenes)
2. **Patrón futuro recomendado** (cuando el proyecto crezca):
   - Separar `models.py` en `schemas.py` (Pydantic) y `services.py` (lógica de negocio)
   - Crear `routers/` para separar rutas por dominio
   - Crear `dependencies.py` para inyección de dependencias de FastAPI

---

## 🔮 Roadmap (Funcionalidades Pendientes)

Según el README y las notas del proyecto, las próximas funcionalidades previstas son:

| # | Feature | Estado | Prioridad |
|---|---------|--------|-----------|
| 1 | **Integración con n8n** (Webhooks) | Pendiente de pruebas | Alta |
| 2 | **Persistencia en BD** (SQLite/PostgreSQL) | No iniciado | Alta |
| 3 | **Manejo de errores** (Middleware de excepciones) | No iniciado | Alta |
| 4 | **Clasificador NLP** (IA para urgencia/importancia) | No iniciado | Media |
| 5 | **Limpieza automática** de Q4 | No iniciado | Baja |
| 6 | **Reportes de productividad** semanal | No iniciado | Baja |
| 7 | **Mover tareas entre columnas Kanban** | No implementado en API | Alta |
| 8 | **Eliminar/editar tareas** | No implementado en API | Alta |
| 9 | **Formulario funcional** (ruta `/crear-tarea` del HTML no existe en el backend) | No conectado | Alta |

---

## 🧪 Estrategia de Testing

> **Estado actual: No existen pruebas.** Se debe implementar un framework de testing desde cero.

### Dependencias de Testing Recomendadas

```text
pytest>=8.0
pytest-asyncio>=0.24
httpx>=0.27          # Cliente async para TestClient de FastAPI
pytest-cov>=5.0      # Cobertura de código
```

### Estructura de Directorios de Tests

```text
eisenflow-core/
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures compartidas (app client, datos de prueba)
│   ├── test_models.py         # Tests unitarios de Tarea y MatrizEisenhower
│   ├── test_api.py            # Tests de integración de endpoints
│   └── test_clasificacion.py  # Tests de la lógica de clasificación Eisenhower
```

---

### Tests Unitarios: `test_models.py`

Prueban la lógica de negocio **aislada** del framework HTTP.

| ID | Test | Descripción | Tipo |
|----|------|-------------|------|
| UM-01 | `test_tarea_creacion_defaults` | Verificar que `Tarea` se crea con `estado="To Do"` y `cuadrante=""` por defecto | Unitario |
| UM-02 | `test_tarea_campos_requeridos` | Verificar que `id`, `titulo`, `urgente`, `importante` son obligatorios | Unitario |
| UM-03 | `test_tarea_validacion_tipos` | Verificar que tipos incorrectos lanzan `ValidationError` | Unitario |
| UM-04 | `test_matriz_inicializa_tablero_vacio` | Verificar que `MatrizEisenhower()` crea tablero con 3 columnas vacías | Unitario |
| UM-05 | `test_clasificar_q1_urgente_importante` | `urgente=True, importante=True` → `"Hacer (Q1)"` | Unitario |
| UM-06 | `test_clasificar_q2_no_urgente_importante` | `urgente=False, importante=True` → `"Programar (Q2)"` | Unitario |
| UM-07 | `test_clasificar_q3_urgente_no_importante` | `urgente=True, importante=False` → `"Delegar (Q3)"` | Unitario |
| UM-08 | `test_clasificar_q4_no_urgente_no_importante` | `urgente=False, importante=False` → `"Eliminar (Q4)"` | Unitario |
| UM-09 | `test_clasificar_agrega_a_todo` | Después de clasificar, la tarea aparece en `tablero_kanban["To Do"]` | Unitario |
| UM-10 | `test_clasificar_multiples_tareas` | Clasificar N tareas y verificar que todas están en el tablero | Unitario |

---

### Tests de Integración: `test_api.py`

Prueban los endpoints HTTP de FastAPI usando `TestClient` (httpx).

| ID | Test | Descripción | Tipo |
|----|------|-------------|------|
| IA-01 | `test_root_endpoint` | `GET /` retorna 200 y mensaje de bienvenida | Integración |
| IA-02 | `test_clasificar_tarea_valida` | `POST /tarea/clasificar` con JSON válido retorna 200 y tarea con cuadrante | Integración |
| IA-03 | `test_clasificar_tarea_body_invalido` | `POST /tarea/clasificar` con JSON incompleto retorna 422 | Integración |
| IA-04 | `test_clasificar_tarea_tipos_incorrectos` | `POST /tarea/clasificar` con tipos erróneos retorna 422 | Integración |
| IA-05 | `test_tablero_vacio_inicial` | `GET /tablero` retorna tablero con 3 columnas vacías | Integración |
| IA-06 | `test_tablero_despues_de_clasificar` | Crear tarea → `GET /tablero` contiene la tarea en "To Do" | Integración |
| IA-07 | `test_flujo_completo_multiples_tareas` | Crear varias tareas → verificar todas en tablero con cuadrantes correctos | Integración |
| IA-08 | `test_response_model_tarea` | Verificar que la respuesta de `/tarea/clasificar` tiene todos los campos del modelo | Integración |

---

### Tests de Regresión (Proteger Funcionalidad Existente)

Estos tests deben ejecutarse **siempre** antes de mergear cambios para asegurar que nada se rompe:

| ID | Test | Qué protege |
|----|------|-------------|
| RG-01 | `test_clasificacion_determinista` | La misma combinación de flags siempre produce el mismo cuadrante |
| RG-02 | `test_estado_default_to_do` | Nuevas tareas siempre inician en "To Do" |
| RG-03 | `test_cuadrante_default_vacio` | El cuadrante por defecto es string vacío antes de clasificar |
| RG-04 | `test_tablero_estructura_kanban` | El tablero siempre tiene exactamente las 3 columnas esperadas |
| RG-05 | `test_api_docs_accesible` | `GET /docs` retorna 200 (Swagger UI funciona) |
| RG-06 | `test_api_openapi_schema` | `GET /openapi.json` retorna esquema válido |

---

### Tests Futuros (Para Nuevas Features)

A medida que se implementen nuevas funcionalidades, agregar los siguientes tests:

#### Persistencia (Base de Datos)
| ID | Test | Descripción |
|----|------|-------------|
| DB-01 | `test_tarea_persiste_en_bd` | Crear tarea → reiniciar app → tarea sigue existiendo |
| DB-02 | `test_tarea_id_autoincremental` | IDs se asignan automáticamente sin colisiones |
| DB-03 | `test_migración_esquema` | Verificar que migraciones de BD se ejecutan correctamente |

#### Mover Tareas en Kanban
| ID | Test | Descripción |
|----|------|-------------|
| KN-01 | `test_mover_tarea_todo_a_in_progress` | Mover tarea de "To Do" a "In Progress" |
| KN-02 | `test_mover_tarea_in_progress_a_done` | Mover tarea de "In Progress" a "Done" |
| KN-03 | `test_mover_tarea_invalida_404` | Mover tarea con ID inexistente retorna 404 |
| KN-04 | `test_mover_tarea_estado_invalido` | Mover a un estado que no existe retorna 422 |

#### Integración con n8n (Webhooks)
| ID | Test | Descripción |
|----|------|-------------|
| WH-01 | `test_webhook_se_dispara_al_clasificar` | Al clasificar, se envía POST al webhook de n8n |
| WH-02 | `test_webhook_payload_correcto` | El JSON enviado al webhook contiene los campos esperados |
| WH-03 | `test_webhook_falla_no_rompe_api` | Si el webhook falla, la API sigue funcionando (graceful degradation) |

#### Manejo de Errores
| ID | Test | Descripción |
|----|------|-------------|
| ER-01 | `test_error_handler_validation_error` | Errores de validación retornan JSON estructurado |
| ER-02 | `test_error_handler_500` | Errores internos retornan JSON con mensaje genérico |
| ER-03 | `test_cors_headers` | Verificar que CORS está correctamente configurado |

---

### Fixture Compartida: `conftest.py`

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Cliente HTTP de prueba para la API de EisenFlow."""
    return TestClient(app)

@pytest.fixture
def tarea_q1():
    """Tarea urgente e importante (Cuadrante Q1 - Hacer)."""
    return {
        "id": 1,
        "titulo": "Resolver bug crítico en producción",
        "urgente": True,
        "importante": True
    }

@pytest.fixture
def tarea_q2():
    """Tarea importante pero no urgente (Cuadrante Q2 - Programar)."""
    return {
        "id": 2,
        "titulo": "Diseñar arquitectura del nuevo módulo",
        "urgente": False,
        "importante": True
    }

@pytest.fixture
def tarea_q3():
    """Tarea urgente pero no importante (Cuadrante Q3 - Delegar)."""
    return {
        "id": 3,
        "titulo": "Responder correos pendientes",
        "urgente": True,
        "importante": False
    }

@pytest.fixture
def tarea_q4():
    """Tarea no urgente ni importante (Cuadrante Q4 - Eliminar)."""
    return {
        "id": 4,
        "titulo": "Organizar carpeta de descargas",
        "urgente": False,
        "importante": False
    }
```

---

### Ejecución de Tests

```bash
# Activar entorno virtual
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/macOS

# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx pytest-cov

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ -v --cov=app --cov-report=term-missing

# Ejecutar solo tests unitarios
pytest tests/test_models.py -v

# Ejecutar solo tests de integración
pytest tests/test_api.py -v

# Ejecutar solo tests de regresión
pytest tests/ -v -k "regression or RG"
```

---

## ⚠️ Problemas Conocidos y Deuda Técnica

| # | Problema | Severidad | Notas |
|---|----------|-----------|-------|
| 1 | **No hay persistencia**: todo el estado se pierde al reiniciar el servidor | Alta | Roadmap item #2 |
| 2 | **Ruta `/crear-tarea` no existe**: el formulario HTML apunta a una ruta que no está implementada en `main.py` | Alta | El formulario del dashboard no funciona |
| 3 | **No hay validación de IDs duplicados**: se pueden crear múltiples tareas con el mismo `id` | Media | Problema hasta que haya BD |
| 4 | **No se pueden mover tareas entre columnas**: falta endpoint de actualización de estado | Alta | Core feature pendiente |
| 5 | **No se pueden eliminar tareas**: falta endpoint DELETE | Media | — |
| 6 | **No hay manejo de errores centralizado**: no hay middleware de excepciones | Media | Roadmap item #3 |
| 7 | **No hay CORS configurado**: impedirá consumo desde frontend separado | Media | — |
| 8 | **Bootstrap CDN con URL incorrecta**: el CSS en `index.html` apunta a `.../modern/bootstrap.min.css` que puede no existir | Baja | Verificar |
| 9 | **Sin tests**: no existe ningún test automatizado | Alta | Este documento define la estrategia |
| 10 | **Sin `.gitignore`**: falta archivo para excluir `.venv/`, `__pycache__/`, etc. | Baja | Crear al iniciar |

---

## 🚀 Cómo Arrancar el Proyecto Localmente

```bash
# 1. Clonar y entrar al directorio
cd eisenflow-core

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate          # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar servidor de desarrollo
uvicorn app.main:app --reload

# 5. Abrir en navegador
# API Docs:  http://127.0.0.1:8000/docs
# Tablero:   http://127.0.0.1:8000/  (requiere ruta de renderizado Jinja2)
```

---

## 📝 Flujo de Trabajo para Agentes

1. **Antes de modificar código**: Leer este archivo y entender la arquitectura.
2. **Antes de agregar features**: Verificar que los tests de regresión existentes pasan.
3. **Al agregar código nuevo**: Escribir tests para la nueva funcionalidad.
4. **Al modificar código existente**: Asegurar que los tests existentes siguen pasando.
5. **Al agregar dependencias**: Actualizar `requirements.txt`.
6. **Al terminar**: Ejecutar la suite completa de tests con cobertura.

---

*Generado para el proyecto EisenFlow Core — Desarrollado por Wilmer Planchez*
