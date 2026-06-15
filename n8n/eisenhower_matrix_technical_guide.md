# Eisenhower Matrix n8n – Guía Técnica

## 📖 Visión General
Este documento describe la **configuración**, **credenciales** y **pruebas unitarias** necesarias para que el workflow de n8n gestione la matriz de Eisenhower y envíe los resultados a los destinos apropiados (Discord, Google Calendar, Gmail y Google Sheets).

---

## 🛠️ Requisitos previos
- n8n ejecutándose en `http://localhost:5678`
- Credenciales de servicio para los siguientes integraciones:
  - **Discord**: Bot token y ID del canal.
  - **Google Calendar**: OAuth client ID/secret y ID del calendario.
  - **Gmail**: SMTP host, puerto, usuario y contraseña de aplicación (App Password).
  - **Google Sheets**: Service‑account JSON y Spreadsheet ID.
- Node **Validate Payload** con el script JavaScript provisto en el flujo.
- Node **Switch** configurado con las rutas `Q1‑Q4`.

---

## ⚙️ Configuración del Workflow
### 1️⃣ Webhook
- **Tipo**: `POST`
- **Path**: `eisenhower/tasks`
- **Respuesta**: `202 Accepted` si la validación pasa; `400 Bad Request` en caso contrario.

### 2️⃣ Validate Payload (Node Code)
```javascript
// Validación básica del payload
const data = $json;
if (!data.id || !data.titulo || !data.cuadrante) {
  throw new Error('Missing required fields');
}
// UUIDv4 regex
if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(data.id)) {
  throw new Error('Invalid UUIDv4');
}
return data;
```

### 3️⃣ Switch (enrutamiento por cuadrante)
| Cuadrante | Nodo destino |
|-----------|--------------|
| `Q1` (Hacer) | Discord/Slack |
| `Q2` (Programar) | Google Calendar |
| `Q3` (Delegar) | Gmail (SMTP) |
| `Q4` (Eliminar) | Google Sheets |

### 4️⃣ Discord / Slack (Node Discord)
- **Token**: `{{ $env.DISCORD_TOKEN }}`
- **Channel ID**: `{{ $env.DISCORD_Q1_CHANNEL }}`
- **Mensaje**:
  ```
  📌 **Tarea:** {{ $json.titulo }}\n🆔 **ID:** {{ $json.id }}\n⏰ **Fecha:** {{ $now.toISO() }}
  ```
- **Retry**: 3 intentos, `exponentialBackoff` con 2 s base.

### 5️⃣ Google Calendar (Node Google Calendar)
- **OAuth Credentials**: `{{ $env.GCAL_CLIENT_ID }}`, `{{ $env.GCAL_CLIENT_SECRET }}`
- **Calendario**: `{{ $env.GCAL_CALENDAR_ID }}`
- **Evento**: duración 1 h, hora de inicio `{{ $now.add(1, 'hour').toISO() }}`.
- **Retry**: 3 intentos, `linearBackoff` 5 s.

### 6️⃣ Gmail (Node SMTP)
- **Host**: `{{ $env.SMTP_HOST }}`
- **Puerto**: `{{ $env.SMTP_PORT }}`
- **Usuario**: `{{ $env.SMTP_USER }}`
- **Contraseña**: `{{ $env.SMTP_PASS }}` (App Password)
- **Asunto**: `Nueva tarea delegada – {{ $json.titulo }}`
- **Cuerpo**: incluye ID, cuadrante y timestamp.
- **Retry**: 2 intentos, `fixedBackoff` 3 s.

### 7️⃣ Google Sheets (Node Google Sheets)
- **Service‑account JSON**: ruta `{{ $env.GSHEETS_SERVICE_ACCOUNT }}`
- **Spreadsheet ID**: `{{ $env.GSHEETS_SPREADSHEET_ID }}`
- **Hoja**: `Eisenhower`
- **Operación**: `Append` fila con `id`, `titulo`, `cuadrante`, `timestamp`.
- **Retry**: 3 intentos, `exponentialBackoff` 1 s.

---

## ✅ Pruebas Unitarias
### 2.1 Webhook & Validación
```bash
curl -X POST http://localhost:5678/webhook-test/eisenhower/tasks \
  -H "Content-Type: application/json" \
  -d '{"id":"123e4567-e89b-12d3-a456-426614174000","titulo":"Revisar informe","cuadrante":"Q1"}'
```
- **Esperado**: `202` y el payload pasa al Switch.
- **Fallo** (campo faltante): `400`.

### 2.2 Rutas Q1‑Q4
Para cada cuadrante, usar el mismo `curl` cambiando `"cuadrante":"Qx"` y verificar:
- **Q1** → mensaje en Discord/Slack (consulta el canal).
- **Q2** → evento creado en Google Calendar (ver en UI).
- **Q3** → correo recibido en la cuenta Gmail configurada.
- **Q4** → nueva fila en Google Sheets (revisar hoja).

### 2.3 Retrys & Tolerancia a Fallos
1. **Desconectar temporalmente** la red o revocar credenciales.
2. Ejecutar la petición del cuadrante correspondiente.
3. Verificar en los logs de n8n que el nodo muestra *retry* y, tras superar los intentos, marque el error sin romper el flujo.

---

## 🛡️ Solución de Problemas
| Síntoma | Posible causa | Acción | 
|---------|----------------|--------|
| No se envía mensaje a Discord | Token o Channel ID incorrectos | Verifica `DISCORD_TOKEN` y `DISCORD_Q1_CHANNEL` en **Credenciales**. |
| Error 401 en Google Calendar | OAuth expirado | Regenera el refresh token o vuelve a autorizar. |
| Gmail no recibe mensaje | Credenciales SMTP erróneas o bloqueado por Google | Revisa `SMTP_USER`/`SMTP_PASS` y permite "Acceso a apps menos seguras" o usa App Password. |
| No se inserta fila en Sheets | Spreadsheet ID o service‑account inválidos | Comprueba que la cuenta del service‑account tiene permiso **Editor** en el Sheet. |

---

## 📦 Deploy & CI
1. **Variables de entorno** en `docker-compose.yml` o `.env` para todas las credenciales.
2. **Test script** (`test.sh`) que ejecuta los *curl* anteriores y valida códigos de respuesta.
3. **Pipeline** (GitHub Actions) que levanta n8n con `docker compose up -d`, ejecuta `test.sh` y aborta si alguna prueba falla.

---

## 📚 Referencias
- n8n Docs – [Webhook Node](https://docs.n8n.io/nodes/n8n-core-nodes/n8n-node-webhook/)
- Discord API – [Send Message](https://discord.com/developers/docs/resources/channel#create-message)
- Google Calendar API – [Events: insert](https://developers.google.com/calendar/api/v3/reference/events/insert)
- Gmail SMTP – [Google SMTP Settings](https://support.google.com/a/answer/176600?hl=en)
- Google Sheets API – [Append Values](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append)
