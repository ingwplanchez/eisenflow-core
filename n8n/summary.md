# ✅ Lo que ya está funcionando

- **Webhook**: La petición desde Postman llegó a n8n (`http://localhost:5678/webhook-test/eisenhower/tasks`) y el payload se mostró en la sección **Body** del registro.
- **Validación**: El nodo *Validate Payload* aceptó los campos `id`, `titulo` y `cuadrante`.
- **Ruta completa**: `http://localhost:5678/webhook-test/eisenhower/tasks` proviene de:
  1. **http://localhost:5678** – tu instancia local de n8n.
  2. **/webhook‑test/** – prefijo que n8n añade cuando ejecutas *Test Workflow*.
  3. **eisenhower/tasks** – el **Path** configurado en el nodo *Webhook* del flujo.

---

## 📲 Configurar salidas a Discord según el cuadrante (Q1‑Q4)

1. **Abre el nodo *Switch* “Route by Quadrant”.**
   - Está configurado para evaluar el campo `{{$json["cuadrante"]}}`.
2. **Crea 4 ramas** (si aún no existen):
   - **Case = "Q1"**
   - **Case = "Q2"**
   - **Case = "Q3"**
   - **Case = "Q4"**
3. **Añade un nodo *Discord* a cada rama** (puedes duplicar uno y arrastrarlo a cada caso).
   - **Operation → Send Message**.
4. **Configura el mensaje y el canal en cada nodo Discord** usando expresiones para que el contenido sea dinámico:

| Cuadrante | Canal (ID) | Mensaje de ejemplo |
|-----------|------------|----------------------|
| Q1 | `{{ $json.channelIdQ1 }}` *(o el ID fijo del canal)* | `{{ "🟢 **Tarea urgente (Q1)**\nTítulo: " + $json.titulo }}` |
| Q2 | `{{ $json.channelIdQ2 }}` | `{{ "🟡 **Tarea importante (Q2)**\nTítulo: " + $json.titulo }}` |
| Q3 | `{{ $json.channelIdQ3 }}` | `{{ "🔵 **Tarea programada (Q3)**\nTítulo: " + $json.titulo }}` |
| Q4 | `{{ $json.channelIdQ4 }}` | `{{ "⚪ **Tarea delegada (Q4)**\nTítulo: " + $json.titulo }}` |

- **Channel ID**: si ya tienes los IDs de tus canales de Discord, ponlos directamente (ej.: `123456789012345678`).
- Si prefieres almacenarlos en una variable **Workflow**, crea una **Set** al inicio del flujo con los IDs y referencia `{{$node["Set"].json.channelIdQ1}}`, etc.
5. **Opcional – Mensaje de confirmación**
   Después de cada nodo Discord, puedes conectar un nodo *Set* que añada `status: "enviado"` y luego un *Respond to Webhook* para que la respuesta HTTP sea `202 Accepted` con `"status":"enviado"`.
6. **Guarda y prueba**
   - En n8n, pulsa **Execute Workflow** → **Test** y envía de nuevo la petición desde Postman.
   - Verifica que el mensaje aparezca en el canal Discord correspondiente.

---

## 🛠️ Tips rápidos

- **Activar la expresión del campo**: en cada nodo Discord, haz clic en la caja del **Channel ID** y elige **Expression** (ícono `{{ }}`) antes de pegar la expresión.
- **Depuración**: añade un nodo *Debug* justo después del Switch para inspeccionar qué valor de `cuadrante` está llegando.
- **Variables de entorno**: si sueles mover los flujos entre entornos, guarda los IDs de los canales como **Credentials → Discord** o como **Environment Variables** y referencia con `{{$env["DISCORD_Q1"]}}`, etc.

---

### 🎉 Próximos pasos sugeridos
1. Añade los nodos Discord a cada caso del Switch (si no lo has hecho).
2. Configura los IDs de canales y los mensajes con las expresiones mostradas.
3. Ejecuta una prueba desde Postman y revisa que el mensaje se publique en el canal correcto.

¿Todo claro? Avísame si necesitas ayuda para crear los nodos Discord o para definir los IDs de tus canales.
