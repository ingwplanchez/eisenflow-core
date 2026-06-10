# EisenFlow Core API

**EisenFlow Core** es un microservicio desarrollado en Python con FastAPI que implementa la lógica de gestión de prioridades basada en la Matriz de Eisenhower y un flujo de trabajo tipo Kanban. Este proyecto actúa como el "cerebro" de un sistema de productividad diseñado para reducir la sobrecarga cognitiva en entornos de ingeniería y consultoría.

## 🚀 Arquitectura del Proyecto

El proyecto sigue una estructura modular y profesional de paquetes en Python:

```text
eisenflow-core/
├── app/
│   ├── __init__.py    # Define la carpeta como paquete Python
│   ├── templates/     # Aquí van tus archivos .html (con Jinja)
│   ├── static/        # Aquí va tu archivo de Bootstrap (css/bootstrap.min.css)
│   ├── main.py        # Punto de entrada de FastAPI y rutas de la API
│   └── models.py      # Lógica POO (Matriz de Eisenhower y Tareas)
├── venv/              # Entorno virtual aislado
└── requirements.txt   # Dependencias del proyecto
```

## 🛠️ Tecnologías Utilizadas

* Python 3.10+: Lenguaje base del proyecto.
* FastAPI: Framework web de alto rendimiento para construir APIs asíncronas.
* Pydantic: Validación de datos y esquemas mediante tipos de Python.
* Uvicorn: Servidor ASGI de alto desempeño para la ejecución del servicio.

## 📋 Funcionalidades Actuales

- [x] Clasificación Automática: Algoritmo que asigna tareas a los cuadrantes de Eisenhower (Hacer, Programar, Delegar, Eliminar) basado en urgencia e importancia.
- [x] Tablero Kanban: Almacenamiento en memoria de las tareas organizadas por estado (To Do, In Progress, Done).
- [x] Documentación Interactiva: Generación automática de Swagger UI (/docs) y ReDoc (/redoc).

---

## 🖥️ Interfaz de Usuario y Orquestación (En Desarrollo)
Para mejorar la interacción del sistema y permitir una comunicación bidireccional, estamos integrando los siguientes requerimientos:

### 1. Front-end Nativo (Jinja2 + Bootstrap)
* **Interfaz de Gestión**: Desarrollo de un Dashboard basado en HTML5, CSS y Bootstrap 5 para una visualización responsiva del tablero Kanban.

* **Renderizado con Jinja2**: Implementación del motor de plantillas de Python para servir las páginas dinámicamente desde el backend de FastAPI.

* **Experiencia de Usuario (UX)**: Diseño de un formulario intuitivo para la entrada de tareas con validación en tiempo real.

### 2. Orquestación de Flujos (Comunicación con n8n)
* **Integración Webhook**: Configuración de un servicio intermedio que capture las acciones del usuario en la interfaz (como "Crear Tarea" o "Mover al Kanban") y las envíe vía POST a un webhook de n8n.

* **Arquitectura de Respuesta**: Implementación de un flujo de espera (Polling/Async) donde la interfaz aguarda la confirmación del webhook de n8n para actualizar el estado del Kanban, asegurando consistencia entre la API y la automatización.

### 3. Diseño del Flujo en n8n
Imagina que cada vez que presionas "Guardar Tarea" en tu interfaz, tu API no solo la guarda, sino que le avisa a n8n. Este es el flujo que deberías montar en n8n:

* **Nodo Webhook (POST)**: Recibe el JSON completo de la tarea desde tu API (id, titulo, cuadrante).

- **Nodo Switch (Decisor)**: Analiza el campo cuadrante.

    * **Si es "Hacer (Q1)"**: Envía una notificación inmediata a tu Telegram o Slack.

    * **Si es "Programar (Q2)"**: Crea un evento automáticamente en tu Google Calendar.

    * **Si es "Delegar (Q3)"**: Envía un correo electrónico pre-redactado (puedes usar un modelo de IA para redactarlo antes de enviarlo).

    * **Si es "Eliminar (Q4)"** : Archiva la información en un Google Sheets de "Tareas Descartadas" (por si acaso).

**Documentación**:
* [n8n-kills: github.com](https://github.com/czlonkowski/n8n-skills)

* [n8n-mcp: github.com](https://github.com/czlonkowski/n8n-mcp)

* [n8n-mcp: Antigravity Setup](https://github.com/czlonkowski/n8n-mcp/blob/main/docs/ANTIGRAVITY_SETUP.md)

* [Antigravity Setup: Youtube](https://youtu.be/FvSySNkkZPc?si=RLpMKrgaKKS5kQ5O)

* [n8n-mcp: Claude Code Setup](https://github.com/czlonkowski/n8n-mcp/blob/main/docs/CLAUDE_CODE_SETUP.md)

* [Claude Code Setup: Youtube](https://youtu.be/DPB4hdLYRc0?si=KREN_60fsfFrfIP4)

---
## 🔮 Próximos Pasos y Mejoras (Roadmap)

1. Integración con n8n (Pendiente de Pruebas)
* Crear flujo en n8n
* Integración del Webhook.
* Arquitectura de la respuesta

2. Optimización con Antigravity/Claude Code
* Refactorización Asíncrona: Utilizar Claude Code para implementar persistencia en base de datos (SQLite/PostgreSQL) de forma asíncrona.
* Manejo de Errores: Implementar middlewares robustos para capturar excepciones de entrada de datos.

3. Inteligencia Artificial (IA)
* Clasificador NLP: Integrar un modelo de lenguaje que determine automáticamente la urgencia e importancia analizando el texto de la tarea, eliminando la necesidad de que el usuario lo marque manualmente.

4. Automatización con Antigravity (Opcional)
* Scripts de Limpieza: Crear un proceso automático que "limpie" el cuadrante de tareas "Eliminar (Q4)" cada medianoche.
* Reportes de Energía: Generar estadísticas semanales sobre cuántas tareas se completaron en el cuadrante de "Programar (Q2)" para medir la eficiencia preventiva.

---

## 🔧 Ejecución Local
1. Activar el entorno virtual:

```bash
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Iniciar el servidor:

```bash
uvicorn app.main:app --reload
```

-----

## 📄 Licencia

Este proyecto está bajo la licencia [MIT](https://es.wikipedia.org/wiki/Licencia_MIT), lo que permite su uso y modificación libremente, siempre que se otorgue el debido crédito.

-----

Desarrollado por Wilmer Planchez Ingeniero de Soluciones AI-Native