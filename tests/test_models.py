import pytest
from pydantic import ValidationError
from app.models import Tarea, MatrizEisenhower

def test_tarea_creacion_defaults():
    """UM-01: Verificar que Tarea se crea con estado='To Do' y cuadrante='' por defecto."""
    tarea = Tarea(id="test-id", titulo="Test Tarea", urgente=True, importante=True)
    assert tarea.estado == "To Do"
    assert tarea.cuadrante == ""

def test_tarea_campos_requeridos():
    """UM-02: Verificar que titulo, urgente, importante son obligatorios."""
    with pytest.raises(ValidationError):
        # Falta titulo
        Tarea(id="id-1", urgente=True, importante=True)
    with pytest.raises(ValidationError):
        # Falta urgente
        Tarea(id="id-1", titulo="Test Tarea", importante=True)
    with pytest.raises(ValidationError):
        # Falta importante
        Tarea(id="id-1", titulo="Test Tarea", urgente=True)

def test_tarea_validacion_tipos():
    """UM-03: Verificar que tipos incorrectos lanzan ValidationError."""
    with pytest.raises(ValidationError):
        # urgente debe ser bool
        Tarea(id="id-1", titulo="Test Tarea", urgente="No es bool", importante=True)

def test_matriz_inicializa_tablero_vacio():
    """UM-04: Verificar que MatrizEisenhower() crea tablero con 3 columnas vacías."""
    matriz = MatrizEisenhower()
    assert "To Do" in matriz.tablero_kanban
    assert "In Progress" in matriz.tablero_kanban
    assert "Done" in matriz.tablero_kanban
    assert len(matriz.tablero_kanban["To Do"]) == 0
    assert len(matriz.tablero_kanban["In Progress"]) == 0
    assert len(matriz.tablero_kanban["Done"]) == 0

def test_clasificar_q1_urgente_importante(tarea_q1):
    """UM-05: urgente=True, importante=True -> 'Hacer (Q1)'."""
    matriz = MatrizEisenhower()
    tarea = Tarea(**tarea_q1)
    tarea_procesada = matriz.clasificar_tarea(tarea)
    assert tarea_procesada.cuadrante == "Hacer (Q1)"

def test_clasificar_q2_no_urgente_importante(tarea_q2):
    """UM-06: urgente=False, importante=True -> 'Programar (Q2)'."""
    matriz = MatrizEisenhower()
    tarea = Tarea(**tarea_q2)
    tarea_procesada = matriz.clasificar_tarea(tarea)
    assert tarea_procesada.cuadrante == "Programar (Q2)"

def test_clasificar_q3_urgente_no_importante(tarea_q3):
    """UM-07: urgente=True, importante=False -> 'Delegar (Q3)'."""
    matriz = MatrizEisenhower()
    tarea = Tarea(**tarea_q3)
    tarea_procesada = matriz.clasificar_tarea(tarea)
    assert tarea_procesada.cuadrante == "Delegar (Q3)"

def test_clasificar_q4_no_urgente_no_importante(tarea_q4):
    """UM-08: urgente=False, importante=False -> 'Eliminar (Q4)'."""
    matriz = MatrizEisenhower()
    tarea = Tarea(**tarea_q4)
    tarea_procesada = matriz.clasificar_tarea(tarea)
    assert tarea_procesada.cuadrante == "Eliminar (Q4)"

def test_clasificar_agrega_a_todo(tarea_q1):
    """UM-09: Después de clasificar, la tarea aparece en tablero_kanban['To Do']."""
    matriz = MatrizEisenhower()
    tarea = Tarea(**tarea_q1)
    matriz.clasificar_tarea(tarea)
    assert len(matriz.tablero_kanban["To Do"]) == 1
    assert matriz.tablero_kanban["To Do"][0].id == tarea.id

def test_clasificar_multiples_tareas(tarea_q1, tarea_q2):
    """UM-10: Clasificar N tareas y verificar que todas están en el tablero."""
    matriz = MatrizEisenhower()
    t1 = Tarea(**tarea_q1)
    t2 = Tarea(**tarea_q2)
    matriz.clasificar_tarea(t1)
    matriz.clasificar_tarea(t2)
    assert len(matriz.tablero_kanban["To Do"]) == 2
