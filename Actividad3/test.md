# Guía rápida de uso (curl) — API de contenidos

Basado en los **esquemas reales** definidos en `app.py`.

---

## Base URL

- `http://127.0.0.1:8000`

---

## 1) Crear post manual

**POST** `/api/contents`

**Request** (ejemplo):
```bash
curl -X POST http://127.0.0.1:8000/api/contents \
  -H "Content-Type: application/json" \
  -d '{
    "platform":"X",
    "title":"Título",
    "tone":"Casual",
    "content":"Contenido del post...",
    "hashtags":["ai","fastapi"],
    "link":"https://example.com",
    "language":"es",
    "variants":["Variante 1","Variante 2"]
  }'
```

**Notas de validación**:
- `platform` debe estar en `{LinkedIn, X, Instagram, Facebook, TikTok}`.
- `hashtags` se normalizan y deduplican (máx. 10).
- `link` debe ser `http://` o `https://`.
- `content` respeta los límites por plataforma (si aplica).
- `variants` se normaliza como lista (esperada por el schema de creación).

---

## 2) Listar todos los posts

**GET** `/api/contents`

```bash
curl -X GET http://127.0.0.1:8000/api/contents \
  -H "Accept: application/json"
```

---

## 3) Obtener un post por ID

**GET** `/api/contents/{post_id}`

```bash
curl -X GET http://127.0.0.1:8000/api/contents/1 \
  -H "Accept: application/json"
```

> Cambia `1` por el `id` real devuelto por el endpoint de listado.

---

## 4) Actualizar un post

**PUT** `/api/contents/{post_id}`

**Request** (ejemplo):
```bash
curl -X PUT http://127.0.0.1:8000/api/contents/1 \
  -H "Content-Type: application/json" \
  -d '{
    "tone":"Profesional",
    "content":"Nuevo contenido para la actualización...",
    "hashtags":["actualizacion","fastapi"]
  }'
```

> En el schema de actualización, todos los campos son opcionales: se envían solo los que quieres modificar.

---

## 5) Eliminar un post

**DELETE** `/api/contents/{post_id}`

```bash
curl -X DELETE http://127.0.0.1:8000/api/contents/1 \
  -H "Accept: application/json"
```

---

## 6) Generar post con IA (y guardar en BD)

**POST** `/api/contents/generate`

**Request** (ejemplo):
```bash
curl -X POST http://127.0.0.1:8000/api/contents/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"Escribe un post motivacional sobre productividad",
    "platform":"LinkedIn",
    "tone":"Profesional",
    "language":"es",
    "variants":2
  }'
```

**Request schema (importante):**
- `prompt`: string (min 1)
- `platform`: string (debe ser una de las soportadas)
- `tone`: string
- `language`: string opcional
- `variants`: **número** entre 1 y 5 (default 1)

**Notas de ejecución**:
- La IA intenta devolver JSON válido y consistente con el esquema.
- Si la IA falla en JSON o validación, hay reintentos automáticos (tenacity).
- El backend normaliza `hashtags` y `variants` antes de guardar.

---

## 7) Errores típicos (para probar)

### a) Platform inválida

```bash
curl -X POST http://127.0.0.1:8000/api/contents/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"Hola",
    "platform":"UnknownNet",
    "tone":"Profesional"
  }'
```

> Espera **HTTP 422**.

### b) Link inválido

```bash
curl -X POST http://127.0.0.1:8000/api/contents \
  -H "Content-Type: application/json" \
  -d '{
    "platform":"X",
    "title":"Título",
    "tone":"Casual",
    "content":"Contenido...",
    "link":"not-a-url"
  }'
```

> Espera **HTTP 422**.
