# AGENTS.md — EisenFlow Core

> Guía para agentes de IA y colaboradores que trabajen en este proyecto.
> Última actualización: 2026-06-20

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
├── tests/                   # Suite de pruebas automatizadas (unitarias, integración y regresión)
├── .venv/                   # Entorno virtual Python (NO modificar, NO commitear)
├── requirements.txt         # Dependencias del proyecto (generado con pip freeze)
├── notas.txt                # Notas de desarrollo del autor
└── README.md                # Documentación del proyecto
```

### Archivos Clave

| Archivo | Responsabilidad |
|---------|----------------|
| [`main.py`](file:///c:/Users/USER/Documents/wplanchez/Portafolio/Repositorios/FastAPI/eisenflow-core/app/main.py) | Instancia de `FastAPI`, rutas de la API, endpoints CRUD (`GET /`, `POST /crear-tarea`, `PUT /tarea/{id}/mover`, `DELETE /tarea/{id}`, `PUT /tarea/{id}/editar`, `GET /tablero`) y webhook de n8n. |
| [`models.py`](file:///c:/Users/USER/Documents/wplanchez/Portafolio/Repositorios/FastAPI/eisenflow-core/app/models.py) | Modelo `Tarea` (Pydantic BaseModel con ID tipo UUID v4), clase `MatrizEisenhower` con lógica de clasificación, priorización y ordenamiento de columnas Kanban. |
| [`index.html`](file:///c:/Users/USER/Documents/wplanchez/Portafolio/Repositorios/FastAPI/eisenflow-core/app/templates/index.html) | Dashboard HTML con formulario de captura y visualización del tablero Kanban interactivo usando Drag & Drop y modals de edición. |

---

## 🔌 Stack Tecnológico

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje base |
| FastAPI | 0.136.x | Framework web asíncrono |
| Pydantic v2 | 2.13.x | Validación de datos y esquemas |
| Uvicorn | 0.49.x | Servidor ASGI |
| Jinja2 | 3.1.x | Motor de plantillas HTML |
| Bootstrap | 5.3.0 (CDN) | Framework CSS para la UI |
| python-multipart | 0.0.32 | Procesamiento de formularios HTML |
| Requests | 2.34.x | Cliente HTTP (integración con n8n) |

---

## 📡 API Endpoints Existentes

| Método | Ruta | Descripción | Request Body | Response |
|--------|------|-------------|-------------|----------|
| `GET` | `/` | Renderiza el Dashboard Kanban en HTML | — | HTML renderizado (Jinja2) |
| `GET` | `/api/health` | Health check de la API | — | `{"message": "EisenFlow API is running..."}` |
| `POST` | `/crear-tarea` | Procesa el formulario HTML y redirige | Form Data (`titulo`, `urgente`, `importante`) | Redirección 303 a `/` |
| `POST` | `/tarea/clasificar` | Crea y clasifica una tarea vía JSON | `Tarea` (JSON) | `Tarea` con cuadrante asignado |
| `GET` | `/tablero` | Retorna el tablero Kanban completo | — | `Dict[str, List[Tarea]]` |
| `GET` | `/tarea/{tarea_id}` | Obtiene los detalles de una tarea específica | — | `Tarea` (JSON) |
| `PUT` | `/tarea/{tarea_id}/mover` | Cambia la columna de una tarea | Query Param `nuevo_estado` | `Tarea` actualizada |
| `PUT` | `/tarea/{tarea_id}/editar` | Modifica título y propiedades de una tarea | `Tarea` (JSON) | `Tarea` recalculada y actualizada |
| `DELETE` | `/tarea/{tarea_id}` | Elimina una tarea del tablero | — | Mensaje de éxito |

### Modelo `Tarea`

```python
class Tarea(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # UUID v4 autogenerado en formato string
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

---

## 🔮 Roadmap (Funcionalidades Pendientes)

| # | Feature | Estado | Prioridad |
|---|---------|--------|-----------|
| 1 | **Persistencia en BD** (SQLite/PostgreSQL) | No iniciado | Alta |
| 2 | **Manejo de errores** (Middleware de excepciones) | No iniciado | Alta |
| 3 | **CORS Configurado** | No iniciado | Media |
| 4 | **Clasificador NLP** (IA para urgencia/importancia) | No iniciado | Media |
| 5 | **Limpieza automática** de Q4 | No iniciado | Baja |
| 6 | **Reportes de productividad** semanal | No iniciado | Baja |

---

## 🧪 Estrategia de Testing

> **Estado actual: Completado.** Se ha implementado e integrado una suite de pruebas automatizadas con pytest que cubre el 100% de la funcionalidad core.

### Dependencias de Testing Utilizadas

```text
pytest>=9.0.3
pytest-asyncio>=1.4.0
httpx>=0.28.1        # Cliente async para TestClient de FastAPI
pytest-cov>=7.1.0    # Cobertura de código
```

### Estructura de Directorios de Tests

```text
eisenflow-core/
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures compartidas (app client, tareas mockup Q1-Q4)
│   ├── test_models.py         # Tests unitarios del modelo de negocio
│   ├── test_api.py            # Tests de integración de la API (HTTP)
│   └── test_regresion.py      # Tests de regresión para blindar la lógica core
```

---

### Tests Unitarios: `test_models.py`

| ID | Test | Descripción | Tipo |
|----|------|-------------|------|
| UM-01 | `test_tarea_creacion_defaults` | Verificar que `Tarea` se crea con `estado="To Do"` y `cuadrante=""` por defecto | Unitario |
| UM-02 | `test_tarea_campos_requeridos` | Verificar que `titulo`, `urgente`, `importante` son obligatorios | Unitario |
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

| ID | Test | Descripción | Tipo |
|----|------|-------------|------|
| IA-01 | `test_root_endpoint` | `GET /` retorna 200 (HTML renderizado) | Integración |
| IA-02 | `test_clasificar_tarea_valida` | `POST /tarea/clasificar` retorna 200 y JSON con cuadrante asignado | Integración |
| IA-03 | `test_clasificar_tarea_body_invalido` | `POST /tarea/clasificar` con JSON incompleto retorna 422 | Integración |
| IA-04 | `test_clasificar_tarea_tipos_incorrectos` | `POST /tarea/clasificar` con tipos erróneos retorna 422 | Integración |
| IA-05 | `test_tablero_vacio_inicial` | `GET /tablero` retorna tablero con 3 columnas vacías | Integración |
| IA-06 | `test_tablero_despues_de_clasificar` | Crear tarea → `GET /tablero` contiene la tarea en "To Do" | Integración |
| IA-07 | `test_flujo_completo_multiples_tareas` | Crear varias tareas → verificar todas en tablero con cuadrantes correctos | Integración |
| IA-08 | `test_response_model_tarea` | Verificar que la respuesta de `/tarea/clasificar` tiene todos los campos del modelo | Integración |

---

### Tests de Regresión (Proteger Funcionalidad Existente)

| ID | Test | Qué protege |
|----|------|-------------|
| RG-01 | `test_clasificacion_determinista` | La misma combinación de flags siempre produce el mismo cuadrante |
| RG-02 | `test_estado_default_to_do` | Nuevas tareas siempre inician en "To Do" |
| RG-03 | `test_cuadrante_default_vacio` | El cuadrante por defecto es string vacío antes de clasificar |
| RG-04 | `test_tablero_estructura_kanban` | El tablero siempre tiene exactamente las 3 columnas esperadas |
| RG-05 | `test_api_docs_accesible` | `GET /docs` retorna 200 (Swagger UI funciona) |
| RG-06 | `test_api_openapi_schema` | `GET /openapi.json` retorna esquema válido |

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
        "titulo": "Resolver bug crítico en producción",
        "urgente": True,
        "importante": True
    }

@pytest.fixture
def tarea_q2():
    """Tarea importante pero no urgente (Cuadrante Q2 - Programar)."""
    return {
        "titulo": "Diseñar arquitectura del nuevo módulo",
        "urgente": False,
        "importante": True
    }

@pytest.fixture
def tarea_q3():
    """Tarea urgente pero no importante (Cuadrante Q3 - Delegar)."""
    return {
        "titulo": "Responder correos pendientes",
        "urgente": True,
        "importante": False
    }

@pytest.fixture
def tarea_q4():
    """Tarea no urgente ni importante (Cuadrante Q4 - Eliminar)."""
    return {
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
```

---

## ⚠️ Problemas Conocidos y Deuda Técnica

| # | Problema | Severidad | Notas |
|---|----------|-----------|-------|
| 1 | **No hay persistencia**: todo el estado se pierde al reiniciar el servidor | Alta | Roadmap item #1 |

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
# Tablero:   http://127.0.0.1:8000/
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
