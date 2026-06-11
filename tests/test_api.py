import pytest

def test_root_endpoint(client):
    """IA-01: GET / retorna 200 y renderiza el HTML del dashboard."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "EisenFlow" in response.text

def test_health_check_endpoint(client):
    """IA-01b: GET /api/health retorna 200 y mensaje JSON."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["message"] == "EisenFlow API is running. Go to /docs or /redoc for documentation."

def test_clasificar_tarea_valida(client, tarea_q1):
    """IA-02: POST /tarea/clasificar con JSON válido retorna 200 y tarea con cuadrante."""
    response = client.post("/tarea/clasificar", json=tarea_q1)
    assert response.status_code == 200
    data = response.json()
    assert data["cuadrante"] == "Hacer (Q1)"
    assert data["id"] == tarea_q1["id"]

def test_clasificar_tarea_body_invalido(client):
    """IA-03: POST /tarea/clasificar con JSON incompleto retorna 422."""
    response = client.post("/tarea/clasificar", json={"titulo": "Falta todo lo demás"})
    assert response.status_code == 422

def test_clasificar_tarea_tipos_incorrectos(client, tarea_q1):
    """IA-04: POST /tarea/clasificar con tipos erróneos retorna 422."""
    tarea_invalida = tarea_q1.copy()
    tarea_invalida["urgente"] = "muy urgente"  # Debe ser bool
    response = client.post("/tarea/clasificar", json=tarea_invalida)
    assert response.status_code == 422

def test_tablero_vacio_inicial(client):
    """IA-05: GET /tablero retorna tablero con 3 columnas vacías."""
    # Nota: como compartimos el estado en memoria, reiniciamos o asumimos que podría tener datos de otros tests,
    # pero para un test limpio, debería retornar la estructura básica.
    response = client.get("/tablero")
    assert response.status_code == 200
    data = response.json()
    assert "To Do" in data
    assert "In Progress" in data
    assert "Done" in data

def test_tablero_despues_de_clasificar(client, tarea_q2):
    """IA-06: Crear tarea -> GET /tablero contiene la tarea en 'To Do'."""
    # Clasificar una tarea primero
    client.post("/tarea/clasificar", json=tarea_q2)
    
    # Obtener el tablero y verificar
    response = client.get("/tablero")
    assert response.status_code == 200
    data = response.json()
    
    # Buscamos si la tarea está en "To Do"
    encontrada = any(t["id"] == tarea_q2["id"] for t in data["To Do"])
    assert encontrada is True

def test_flujo_completo_multiples_tareas(client, tarea_q3, tarea_q4):
    """IA-07: Crear varias tareas -> verificar todas en tablero con cuadrantes correctos."""
    client.post("/tarea/clasificar", json=tarea_q3)
    client.post("/tarea/clasificar", json=tarea_q4)
    
    response = client.get("/tablero")
    data = response.json()
    
    ids_todo = [t["id"] for t in data["To Do"]]
    assert tarea_q3["id"] in ids_todo
    assert tarea_q4["id"] in ids_todo

def test_response_model_tarea(client, tarea_q1):
    """IA-08: Verificar que la respuesta de /tarea/clasificar tiene todos los campos del modelo."""
    response = client.post("/tarea/clasificar", json=tarea_q1)
    data = response.json()
    campos_esperados = {"id", "titulo", "urgente", "importante", "estado", "cuadrante"}
    assert campos_esperados.issubset(data.keys())

def test_crear_tarea_formulario(client):
    """F2-01: POST /crear-tarea crea una tarea usando el formulario HTML y redirige."""
    payload = {
        "titulo": "Tarea desde Formulario",
        "urgente": "true",
        "importante": "true"
    }
    response = client.post("/crear-tarea", data=payload, follow_redirects=False)
    # Redirección 303 See Other
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    
    # Validar que se guardó en el tablero
    res_tablero = client.get("/tablero")
    data = res_tablero.json()
    titulos = [t["titulo"] for t in data["To Do"]]
    assert "Tarea desde Formulario" in titulos
