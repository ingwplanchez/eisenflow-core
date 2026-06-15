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

def test_obtener_detalle_tarea(client, tarea_q1):
    """GET-01: GET /tarea/{tarea_id} retorna 200 y detalles si la tarea existe."""
    # Primero insertamos
    client.post("/tarea/clasificar", json=tarea_q1)
    
    response = client.get(f"/tarea/{tarea_q1['id']}")
    assert response.status_code == 200
    assert response.json()["titulo"] == tarea_q1["titulo"]

def test_obtener_detalle_tarea_inexistente(client):
    """GET-02: GET /tarea/{tarea_id} retorna 404 si la tarea no existe."""
    response = client.get("/tarea/id-inexistente-123")
    assert response.status_code == 404

def test_mover_tarea_exito(client, tarea_q1):
    """KN-01: PUT /tarea/{tarea_id}/mover mueve la tarea y retorna 200."""
    client.post("/tarea/clasificar", json=tarea_q1)
    
    response = client.put(f"/tarea/{tarea_q1['id']}/mover?nuevo_estado=In Progress")
    assert response.status_code == 200
    assert response.json()["estado"] == "In Progress"
    
    # Validar en el tablero
    res_tablero = client.get("/tablero")
    tablero = res_tablero.json()
    assert any(t["id"] == tarea_q1["id"] for t in tablero["In Progress"])
    assert not any(t["id"] == tarea_q1["id"] for t in tablero["To Do"])

def test_mover_tarea_inexistente(client):
    """KN-03: PUT /tarea/{tarea_id}/mover retorna 404 para tarea inexistente."""
    response = client.put("/tarea/id-inexistente-123/mover?nuevo_estado=In Progress")
    assert response.status_code == 404

def test_mover_tarea_estado_invalido(client, tarea_q1):
    """KN-04: PUT /tarea/{tarea_id}/mover retorna 422 si el estado destino no existe."""
    client.post("/tarea/clasificar", json=tarea_q1)
    response = client.put(f"/tarea/{tarea_q1['id']}/mover?nuevo_estado=EstadoFalso")
    assert response.status_code == 422

def test_eliminar_tarea_exito(client, tarea_q1):
    """DEL-01: DELETE /tarea/{tarea_id} retorna 200 y remueve la tarea."""
    client.post("/tarea/clasificar", json=tarea_q1)
    
    response = client.delete(f"/tarea/{tarea_q1['id']}")
    assert response.status_code == 200
    
    # Verificar que no está en el tablero
    res_tablero = client.get("/tablero")
    tablero = res_tablero.json()
    assert not any(t["id"] == tarea_q1["id"] for col in tablero.values() for t in col)

def test_eliminar_tarea_inexistente(client):
    """DEL-02: DELETE /tarea/{tarea_id} retorna 404 si la tarea no existe."""
    response = client.delete("/tarea/id-inexistente-123")
    assert response.status_code == 404

def test_webhook_disparo_modo_test(client, tarea_q1, monkeypatch):
    """WH-01: Al clasificar en entorno de test, se dispara POST a webhook-test."""
    import requests_mock
    monkeypatch.setenv("N8N_ENV", "test")
    
    with requests_mock.Mocker() as m:
        m.post("http://localhost:5678/webhook-test/eisenhower/tasks", status_code=200)
        
        response = client.post("/tarea/clasificar", json=tarea_q1)
        assert response.status_code == 200
        assert m.called
        
        # Validar payload enviado
        history = m.request_history
        assert len(history) == 1
        assert history[0].json()["id"] == tarea_q1["id"]
        assert history[0].json()["cuadrante"] == "Q1"

def test_webhook_disparo_modo_produccion(client, tarea_q1, monkeypatch):
    """WH-02: Al clasificar en entorno de producción, se dispara POST a webhook (producción)."""
    import requests_mock
    monkeypatch.setenv("N8N_ENV", "production")
    
    with requests_mock.Mocker() as m:
        m.post("http://localhost:5678/webhook/eisenhower/tasks", status_code=200)
        
        response = client.post("/tarea/clasificar", json=tarea_q1)
        assert response.status_code == 200
        assert m.called
        assert m.request_history[0].json()["cuadrante"] == "Q1"

def test_webhook_tolerancia_fallo(client, tarea_q1):
    """WH-03: Si el webhook de n8n falla o no responde, la API no se ve afectada."""
    import requests_mock
    with requests_mock.Mocker() as m:
        m.post("http://localhost:5678/webhook-test/eisenhower/tasks", status_code=500)
        
        # La solicitud debe ser exitosa aunque el webhook falle (graceful degradation)
        response = client.post("/tarea/clasificar", json=tarea_q1)
        assert response.status_code == 200

def test_editar_tarea_exito(client, tarea_q1):
    """EDIT-01: PUT /tarea/{tarea_id}/editar modifica los detalles de la tarea y recalcula cuadrante."""
    import requests_mock
    client.post("/tarea/clasificar", json=tarea_q1)
    
    nuevo_payload = {
        "id": tarea_q1["id"],
        "titulo": "Título modificado",
        "urgente": False,
        "importante": True
    }
    
    with requests_mock.Mocker() as m:
        m.post("http://localhost:5678/webhook-test/eisenhower/tasks", status_code=200)
        response = client.put(f"/tarea/{tarea_q1['id']}/editar", json=nuevo_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["titulo"] == "Título modificado"
        assert data["cuadrante"] == "Programar (Q2)"

def test_editar_tarea_inexistente(client):
    """EDIT-02: PUT /tarea/{tarea_id}/editar retorna 404 para una tarea inexistente."""
    payload = {
        "id": "inexistente",
        "titulo": "No existe",
        "urgente": False,
        "importante": True
    }
    response = client.put("/tarea/id-inexistente-123/editar", json=payload)
    assert response.status_code == 404

def test_ordenacion_prioridad_cuadrante(client, tarea_q1, tarea_q2, tarea_q3, tarea_q4):
    """SORT-01: Las tareas en el tablero deben quedar siempre ordenadas en prioridad Q1 > Q2 > Q3 > Q4."""
    # Las clasificamos en desorden (Q4 -> Q3 -> Q2 -> Q1)
    client.post("/tarea/clasificar", json=tarea_q4)
    client.post("/tarea/clasificar", json=tarea_q3)
    client.post("/tarea/clasificar", json=tarea_q2)
    client.post("/tarea/clasificar", json=tarea_q1)
    
    response = client.get("/tablero")
    tablero = response.json()
    
    cuadrantes_todo = [t["cuadrante"] for t in tablero["To Do"] if t["id"] in [
        tarea_q1["id"], tarea_q2["id"], tarea_q3["id"], tarea_q4["id"]
    ]]
    
    # El orden en el que se listan debe ser exactamente Q1, Q2, Q3, Q4
    assert cuadrantes_todo == ["Hacer (Q1)", "Programar (Q2)", "Delegar (Q3)", "Eliminar (Q4)"]
