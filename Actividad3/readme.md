# Generador de Contenidos IA (FastAPI + SQLite + LLM)

API REST en **FastAPI** que permite:
- Gestionar publicaciones de redes sociales (**CRUD**) en **SQLite** usando **SQLAlchemy**.
- Generar automáticamente una publicación mediante un modelo LLM (vía **Azure OpenAI** o **Ollama**) y guardarla en la base de datos.

El proyecto está implementado en un único archivo: **`app.py`**.

---

## Contenido
- [Características](#características)
- [Estructura del sistema](#estructura-del-sistema)
- [Modelo de datos](#modelo-de-datos)
- [Validaciones y reglas de negocio](#validaciones-y-reglas-de-negocio)
- [Configuración (variables de entorno)](#configuración-variables-de-entorno)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Endpoints](#endpoints)
- [Notas sobre el proveedor de IA](#notas-sobre-el-proveedor-de-ia)
- [Requisitos](#requisitos)

---

## Características

- **CRUD** de publicaciones:
  - Crear manualmente
  - Listar todas
  - Obtener por id
  - Actualizar
  - Eliminar
- Endpoint de **generación con IA**:
  - `POST /api/contents/generate`
  - Construye un prompt para obtener **JSON** con campos esperados
  - Reintenta con **tenacity** si falla (p.ej. JSON inválido)
  - Valida reglas (plataforma, longitud, hashtags, link)
  - Persiste el resultado en SQLite

---

## Estructura del sistema

En `app.py` se usan estos componentes principales:
- **FastAPI**: definición de la API y endpoints.
- **SQLAlchemy 2.0**: modelo `SocialMediaPost` y sesiones (`SessionLocal`).
- **Pydantic v2**: schemas de entrada/salida (validación y respuesta estructurada).
- **LangChain**:
  - `AzureChatOpenAI` si `LLM_PROVIDER=azure`
  - `ChatOllama` si `LLM_PROVIDER=ollama` (o si no es azure y hay `OLLAMA_URL`)
- **tenacity**: reintentos con backoff exponencial.

---

## Modelo de datos

### Tabla: `social_media_posts`

Clase: `SocialMediaPost`
- `id`: `Integer` PK
- `platform`: `String`
- `title`: `String`
- `tone`: `String`
- `content`: `Text`
- `hashtags`: `Text` (se guarda como JSON string)
- `link`: `String` opcional (URL)
- `language`: `String` opcional
- `variants`: `Text` (se guarda como JSON string)
- `created_at`: `DateTime` (default `utcnow`)
- `updated_at`: `DateTime` (auto actualización)

> Nota: `hashtags` y `variants` se almacenan en la BD como texto JSON; al devolverlos al cliente se convierten a `List[str]`.

---

## Validaciones y reglas de negocio

### Plataformas soportadas
`SUPPORTED_PLATFORMS = {"LinkedIn", "X", "Instagram", "Facebook", "TikTok"}`

Si la `platform` no está en el set: **HTTP 422**.

### Longitud máxima por plataforma
`PLATFORM_MAX_LENGTH`:
- `X` → 280
- `LinkedIn` → 3000
- `Instagram` → 2200

Si el `content` supera el máximo (cuando existe regla para esa plataforma): **HTTP 422**.

### Hashtags
- Normalización: asegura que cada hashtag empiece con `#`
- Deduplicación case-insensitive
- Máximo: **10**

Si excede 10: **HTTP 422**.

### Link
- Opcional
- Si se envía debe ser URL con `http://` o `https://` y dominio válido.

Si no cumple: **HTTP 422**.

### Variantes (variants)
- Para entrada de generación: el campo `variants` es un **número** entre 1 y 5.
- Para salida/CRUD: `variants` se maneja como lista de strings (1 a 5) al normalizar.

---

## Configuración (variables de entorno)

El proyecto carga `.env` con `python-dotenv`.

Variables usadas en `app.py`:

### Base de datos
- `DATABASE_URL` (default: `sqlite:///socialmedia.db`)

### Proveedor LLM
- `LLM_PROVIDER` (default: `azure`)

#### Azure OpenAI (si `LLM_PROVIDER=azure`)
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT`

#### Ollama (si `LLM_PROVIDER=ollama` o si no es azure y hay `OLLAMA_URL`)
- `OLLAMA_URL`

### Modelo
- `MODEL_NAME` (default: `gpt-5.4-nano`)

---

## Instalación

1) Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
```

2) Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución

Arranque con Uvicorn:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

También puedes ejecutar directamente:

```bash
python app.py
```

Al iniciar, se crea automáticamente la tabla en SQLite si no existe.

Visión de documentación:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **Redoc**: `http://127.0.0.1:8000/redoc`

---

## Endpoints

### Listar posts
- `GET /api/contents`

**Respuesta**: `SocialMediaPostsSchema`:
```json
{ "items": [ ... ] }
```

### Obtener un post por id
- `GET /api/contents/{post_id}`

### Crear post manual
- `POST /api/contents`

Entrada: `SocialMediaPostCreateSchema`

### Actualizar post
- `PUT /api/contents/{post_id}`

Entrada: `SocialMediaPostUpdateSchema`

### Eliminar post
- `DELETE /api/contents/{post_id}`

### Generar post con IA (y guardar)
- `POST /api/contents/generate`

Entrada: `GeneratePostRequest`

Ejemplo de request:
```json
{
  "prompt": "Genera un post breve para LinkedIn sobre IA en educación",
  "platform": "LinkedIn",
  "tone": "Profesional",
  "language": "es",
  "variants": 3
}
```

**Respuesta**: `SocialMediaPostSchema` con los campos generados.

---

## Notas sobre el proveedor de IA

- El endpoint `/api/contents/generate`:
  1. Valida `platform`.
  2. Construye un prompt para forzar **JSON válido**.
  3. Llama al LLM con mensajes `System` y `Human`.
  4. Parsea el JSON con `json.loads` y valida con el schema `SocialMediaPostSchema`.
  5. Si algo falla (p.ej. JSON inválido), reintenta hasta 3 veces con backoff.

- Aunque se pida `platform` y `tone`, la implementación los “sobrescribe” en la respuesta del LLM para mantener consistencia.

---

## Requisitos

Dependencias declaradas en `requirements.txt`:
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `pydantic`
- `python-dotenv`
- `tenacity`
- `langchain-openai`
- `langchain-ollama`
- `httpx`
- `pytest`

---

## Archivos del workspace
- `.env.example`: ejemplo de configuración (no incluido aquí por restricciones de acceso al contenido).
- `app.py`: aplicación completa.
- `requirements.txt`: dependencias.
- `test.md`: guía rápida para test con Swagger UI
