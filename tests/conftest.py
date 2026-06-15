import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(autouse=True)
def limpiar_matriz():
    """Limpia el estado de la matriz en memoria antes de cada test."""
    from app.main import matriz
    matriz.tablero_kanban["To Do"] = []
    matriz.tablero_kanban["In Progress"] = []
    matriz.tablero_kanban["Done"] = []

@pytest.fixture
def client():
    """Cliente HTTP de prueba para la API de EisenFlow."""
    return TestClient(app)

@pytest.fixture
def tarea_q1():
    """Tarea urgente e importante (Cuadrante Q1 - Hacer)."""
    return {
        "id": "q1-test-id",
        "titulo": "Resolver bug crítico en producción",
        "urgente": True,
        "importante": True
    }

@pytest.fixture
def tarea_q2():
    """Tarea importante pero no urgente (Cuadrante Q2 - Programar)."""
    return {
        "id": "q2-test-id",
        "titulo": "Diseñar arquitectura del nuevo módulo",
        "urgente": False,
        "importante": True
    }

@pytest.fixture
def tarea_q3():
    """Tarea urgente pero no importante (Cuadrante Q3 - Delegar)."""
    return {
        "id": "q3-test-id",
        "titulo": "Responder correos pendientes",
        "urgente": True,
        "importante": False
    }

@pytest.fixture
def tarea_q4():
    """Tarea no urgente ni importante (Cuadrante Q4 - Eliminar)."""
    return {
        "id": "q4-test-id",
        "titulo": "Organizar carpeta de descargas",
        "urgente": False,
        "importante": False
    }
