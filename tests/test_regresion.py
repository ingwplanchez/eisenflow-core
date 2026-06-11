import pytest
from app.models import Tarea, MatrizEisenhower

def test_clasificacion_determinista():
    """RG-01: La misma combinación de flags siempre produce el mismo cuadrante."""
    matriz = MatrizEisenhower()
    
    # Q1
    t1 = Tarea(id="1", titulo="T1", urgente=True, importante=True)
    assert matriz.clasificar_tarea(t1).cuadrante == "Hacer (Q1)"
    
    # Q2
    t2 = Tarea(id="2", titulo="T2", urgente=False, importante=True)
    assert matriz.clasificar_tarea(t2).cuadrante == "Programar (Q2)"
    
    # Q3
    t3 = Tarea(id="3", titulo="T3", urgente=True, importante=False)
    assert matriz.clasificar_tarea(t3).cuadrante == "Delegar (Q3)"
    
    # Q4
    t4 = Tarea(id="4", titulo="T4", urgente=False, importante=False)
    assert matriz.clasificar_tarea(t4).cuadrante == "Eliminar (Q4)"

def test_estado_default_to_do():
    """RG-02: Nuevas tareas siempre inician en 'To Do'."""
    tarea = Tarea(id="5", titulo="T5", urgente=True, importante=True)
    assert tarea.estado == "To Do"

def test_cuadrante_default_vacio():
    """RG-03: El cuadrante por defecto es string vacío antes de clasificar."""
    tarea = Tarea(id="6", titulo="T6", urgente=True, importante=True)
    assert tarea.cuadrante == ""

def test_tablero_estructura_kanban():
    """RG-04: El tablero siempre tiene exactamente las 3 columnas esperadas."""
    matriz = MatrizEisenhower()
    assert list(matriz.tablero_kanban.keys()) == ["To Do", "In Progress", "Done"]

def test_api_docs_accesible(client):
    """RG-05: GET /docs retorna 200 (Swagger UI funciona)."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_api_openapi_schema(client):
    """RG-06: GET /openapi.json retorna esquema válido."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
