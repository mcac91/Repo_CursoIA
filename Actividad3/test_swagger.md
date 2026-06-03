# Guía rápida para test con Swagger UI

Esta API está implementada con **FastAPI**, por lo que su documentación interactiva (Swagger UI) está integrada.

---

## 1) Iniciar el servidor

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

---

## 2) Abrir Swagger UI

Abre en el navegador:

- **Swagger UI**: `http://127.0.0.1:8000/docs`

(Alternativa)
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 3) Cómo testear (paso a paso)

### Paso A — Probar CRUD

1. **GET `/api/contents`**
   - En la pantalla de endpoint, pulsa **Try it out** y luego **Execute**.
   - Verifica que devuelve un JSON con `items`.

2. **POST `/api/contents`** (Crear manual)
   - Pulsa **Try it out**.
   - Rellena el body con un JSON que cumpla `SocialMediaPostCreateSchema`.
   - Campos obligatorios: `platform`, `title`, `tone`, `content`.
   - Campos opcionales: `hashtags`, `link`, `language`, `variants`.
   - Pulsa **Execute**.

   Ejemplo de body (pégalo en Swagger):
   ```json
   {
     "platform": "X",
     "title": "Título",
     "tone": "Casual",
     "content": "Contenido del post...",
     "hashtags": ["ai", "fastapi"],
     "link": "https://example.com",
     "language": "es",
     "variants": ["Variante 1", "Variante 2"]
   }
   ```

3. **GET `/api/contents/{post_id}`**
   - En **Parameters**, indica un `post_id` (usa el `id` que obtuviste en el POST o en el listado).
   - **Try it out** → **Execute**.

4. **PUT `/api/contents/{post_id}`** (Actualizar)
   - En el body puedes enviar SOLO los campos que quieras cambiar (todos son opcionales en `SocialMediaPostUpdateSchema`).
   - Ejemplo: cambia `tone`, `content` y `hashtags`.

5. **DELETE `/api/contents/{post_id}`**
   - Indica `post_id`.
   - Ejecuta el **Execute** y verifica que devuelve **204** (sin body).

---

### Paso B — Probar generación con IA

1. Ve al endpoint **POST `/api/contents/generate`**.

2. Pulsa **Try it out**.

3. Rellena el body con `GeneratePostRequest`:
   - `prompt` (obligatorio)
   - `platform` (obligatorio)
   - `tone` (obligatorio)
   - `language` (opcional)
   - `variants` (opcional pero es **número** entre 1 y 5)

Ejemplo:
```json
{
  "prompt": "Escribe un post motivacional sobre productividad",
  "platform": "LinkedIn",
  "tone": "Profesional",
  "language": "es",
  "variants": 2
}
```

4. Pulsa **Execute**.

5. Comprueba:
   - Que el response cumple `SocialMediaPostSchema`
   - Que `hashtags` viene como lista (en JSON)
   - Que el post se guarda: haz luego **GET `/api/contents`** y verifica que aparece.

---

## 4) Casos negativos rápidos (para validar reglas)

### Platform inválida (debe dar 422)

En **POST `/api/contents/generate`** usa:
```json
{
  "prompt": "Hola",
  "platform": "UnknownNet",
  "tone": "Profesional"
}
```

### Link inválido (debe dar 422) en POST `/api/contents`

```json
{
  "platform": "X",
  "title": "Título",
  "tone": "Casual",
  "content": "Contenido...",
  "link": "not-a-url"
}
```

---

## 5) Checklist final

- [ ] CRUD funciona (POST/GET/PUT/DELETE)
- [ ] Validaciones devuelven HTTP 422 cuando corresponde
- [ ] `/generate` produce respuesta y se persiste en SQLite
- [ ] Swagger muestra schemas y tipos correctos

