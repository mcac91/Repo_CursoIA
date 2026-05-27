# Memoria de Proyecto: Generador de Contenidos IA

Este documento es una guía paso a paso para implementar el proyecto de la actividad 3 del módulo 4, unificando los requisitos de `1-actividad.md` con las decisiones técnicas de `plan.md`.

## 1. Objetivo general

Construir una API REST que genere y almacene publicaciones para redes sociales a partir de un prompt del usuario, con:

- FastAPI
- SQLite
- SQLAlchemy 2.0 o SQLModel
- LangChain + LLM con salida estructurada Pydantic
- Azure OpenAI (`gpt-5.4-nano`) como proveedor recomendado
- Opción alternativa: Ollama local con `ChatOllama`

> Checkpoint 1: valida el stack elegido y la estrategia de proveedor de IA antes de continuar.

> ✅ Checkpoint 1 completado: stack validado con FastAPI, SQLite, SQLAlchemy 2.0, Pydantic v2, Azure OpenAI y entrega en único archivo.

## 2. Stack tecnológico final y arquitectura del entregable

### Stack recomendado

- API REST: `FastAPI`
- Servidor: `uvicorn`
- ORM: `SQLAlchemy 2.0` o `SQLModel`
- Base de datos: `SQLite`
- Validación: `Pydantic v2`
- IA: `AzureChatOpenAI` o `ChatOllama`
- Variables de entorno: `python-dotenv`
- Reintentos: `tenacity`
- Testing: `pytest`

### Archivo único de entrega

La implementación debe quedar en un único archivo Python para facilitar la corrección. Aunque el plan menciona `m3_*`, esta entrega pertenece al módulo 4, por lo que el nombre final debe ser:

- `m4_nombre_apellido.py`

### Estructura interna recomendada

```text
# Imports
# Configuración / variables de entorno
# Base de datos
# Modelos SQLAlchemy / SQLModel
# Schemas Pydantic
# Configuración Azure OpenAI u Ollama
# Servicios IA y reintentos
# CRUD helpers
# Endpoints FastAPI
# Inicialización DB
# Main
```

> Checkpoint 2: confirma que vas a implementar todo en un único archivo y cuál ORM usarás.

## 3. Definición del modelo de datos

Entidad principal: `SocialMediaPost`.

### Campos mínimos obligatorios

- `id`: int, PK auto increment
- `platform`: string
- `title`: string
- `tone`: string
- `content`: text
- `hashtags`: string
- `link`: string opcional
- `created_at`: datetime automático

### Campos adicionales recomendados (opcional)

- `language`
- `variants`
- `updated_at`

> Checkpoint 3: valida el modelo de datos final y si deseas incluir campos extra.

## 4. Schemas Pydantic

Crear al menos dos schemas:

- `SocialMediaPostSchema` para un post individual
- `SocialMediaPostsSchema` para colecciones de posts

### Requisitos clave

- Incluir `model_config = ConfigDict(from_attributes=True)` para convertir objetos de ORM a Pydantic.
- Definir todos los campos necesarios.
- `link` debe ser opcional.
- Opcionalmente, incluir campos como `language` y `variants` si los agregas al modelo.

> Checkpoint 4: revisa y valida los schemas antes de continuar.

## 5. Variables de entorno y configuración

Es importante configurar la aplicación mediante variables de entorno en lugar de valores hardcodeados.

### Variables recomendadas

- `DATABASE_URL=sqlite:///socialmedia.db`
- `AZURE_OPENAI_ENDPOINT=`  (solo si usas Azure)
- `AZURE_OPENAI_API_KEY=`  (solo si usas Azure)
- `AZURE_OPENAI_API_VERSION=`  (solo si usas Azure)
- `AZURE_OPENAI_DEPLOYMENT=`  (solo si usas Azure)
- `OLLAMA_URL=`  (solo si usas Ollama local)
- `MODEL_NAME=gpt-5.4-nano` o `gemma3:1b`

> Checkpoint 5: confirma la configuración de entorno y proveedor de IA elegido.

## 6. Endpoints REST necesarios

Implementar estos endpoints en el archivo único:

- `GET /api/contents` → devuelve todos los posts
- `GET /api/contents/{id}` → devuelve un post por ID
- `POST /api/contents` → crea un post manual sin llamar al LLM
- `PUT /api/contents/{id}` → actualiza un post existente
- `DELETE /api/contents/{id}` → borra un post por ID
- `POST /api/contents/generate` → genera, guarda y devuelve un post usando IA

### Validación CRUD

- Los endpoints CRUD deben operar contra la base de datos.
- El endpoint `/generate` es el único que invoca al modelo.
- La respuesta de los demás endpoints no debe depender de IA.

> Checkpoint 6: valida que el CRUD básico funciona con datos manuales antes de añadir IA.

## 7. Diseño del endpoint `/api/contents/generate`

### Flujo requerido

1. Leer `prompt` desde el JSON de la petición.
2. Instanciar el modelo: `ChatOllama` o `AzureChatOpenAI`.
3. Enlazar el schema Pydantic al modelo con `with_structured_output(SocialMediaPostSchema)`.
4. Llamar al modelo con mensajes de tipo `system` y `human`.
5. Convertir la respuesta en un objeto Pydantic.
6. Guardar el post en la base de datos.
7. Retornar el post al cliente.

### Ejemplo de entrada sugerida

```json
{
  "prompt": "Genera un post breve para LinkedIn sobre IA en educación",
  "platform": "LinkedIn",
  "tone": "Profesional"
}
```

### Recomendaciones de prompt

- El `system` prompt debe explicar qué es un post de red social.
- El `human` prompt debe incluir el texto del usuario y cualquier instrucción adicional.
- Si no se usa `with_structured_output`, entonces usar `PydanticOutputParser`.

> Checkpoint 7: comprueba que `/api/contents/generate` produce salida estructurada y persiste el resultado.

## 8. Generación estructurada y reintentos

### Estructura de salida

La IA debe devolver siempre JSON válido. Esto es clave para la evaluación.

### Reintentos automáticos

Usar `tenacity` para manejar:

- timeouts
- 429 rate limits
- errores 5xx
- JSON inválido

### Estrategia recomendada

```python
retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
```

> Checkpoint 8: valida la lógica de reintentos y la robustez de la llamada al LLM.

## 9. Reglas de negocio y validaciones

### Plataforma admitida

Permitir al menos:

- `LinkedIn`
- `X`
- `Instagram`
- `Facebook`
- `TikTok`

### Longitud de contenido

- `X` ≤ 280 caracteres
- `LinkedIn` ≤ 3000 caracteres
- `Instagram` ≤ 2200 caracteres

### Hashtags

- máximo 10 hashtags
- eliminar duplicados

### Links

- validar formato URL
- opcional

### Variantes

- mínimo 1
- máximo 5

> Checkpoint 9: revisa y aprueba las reglas de negocio que aplicarás en los schemas o en los endpoints.

## 10. Base de datos y creación de tablas

La base de datos debe configurarse para autogenerar la tabla al iniciar la app.

### SQLite + FastAPI

- engine con `check_same_thread=False`
- tablas creadas en el arranque
- `Session` con `yield` y `Depends`

> Checkpoint 10: valida que la configuración de la base de datos crea la tabla correctamente.

## 11. Validación y pruebas locales

Probar todos los endpoints con:

incluye en el fichero @file:pasos-implementacion.md como condición para el agente que debe seguir las reglas definidas en @AGENT_

- `curl` / `httpie`
- Postman
- Swagger UI de FastAPI

### Flujo de pruebas recomendado

1. Crear un post manual con `POST /api/contents`
2. Listar con `GET /api/contents`
3. Leer un post con `GET /api/contents/{id}`
4. Actualizar con `PUT /api/contents/{id}`
5. Borrar con `DELETE /api/contents/{id}`
6. Generar un post con `POST /api/contents/generate`

### Pruebas adicionales

- Verificar que el post generado queda almacenado en la base de datos
- Revisar que los datos devueltos respetan el schema
- Probar casos inválidos (faltan campos, ID no existe, campo url inválido)

> Checkpoint 11: valida cada operación y documenta los resultados en este fichero.

## 12. Documentación y evidencias

Guardar en el proyecto:

- solicitudes usadas
- respuestas obtenidas
- errores resueltos
- decisiones de implementación
- nombre del archivo final

Este fichero debe ser la memoria del proyecto y la guía para un agente IA que continúe el trabajo.

> Checkpoint 12: confirma que la documentación está suficiente para que otro desarrollador / agente IA retome el proyecto.

## 13. Revisión final y entrega

Antes de cerrar el proyecto, verifica:

- nombre del entregable: `m4_nombre_apellido.py`
- endpoints CRUD funcionales
- endpoint `/api/contents/generate` con salida estructurada
- post generado guardado en la base de datos
- variables de entorno definidas y usadas correctamente

### Entrega opcional

Si decides entregar un zip, incluye:

- `m4_nombre_apellido.py`
- `plan.md`
- `pasos-implementacion.md`
- `.env.example`

> Checkpoint 13: valida el entregable final y la estructura del repositorio.

---

## Instrucciones para el agente IA

Este proyecto debe ejecutarse paso a paso con confirmación del desarrollador en cada checkpoint. El agente IA puede proponer implementaciones, sugerir código y ofrecer ejemplos, pero no debe continuar al siguiente paso hasta que el desarrollador valide cada checkpoint.

Cada paso debe ser:

1. Describir brevemente el objetivo.
2. Proponer acciones concretas.
3. Seguir las reglas definidas en `@file:AGENT.md`.
4. Esperar confirmación del desarrollador.
5. Pasar al siguiente paso solo si el checkpoint está validado.
