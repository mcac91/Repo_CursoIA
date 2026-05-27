# Planificación Técnica — Generador de Contenidos IA con FastAPI

Basado en el enunciado del ejercicio  y en tus requisitos técnicos.

---

# 1. Objetivo del Proyecto

Desarrollar una API REST con FastAPI capaz de:

* Gestionar publicaciones para redes sociales.
* Generar contenido mediante IA usando:

  * Microsoft Azure OpenAI
  * modelo `gpt-5.4-nano`
* Almacenar datos en SQLite.
* Generar múltiples variantes de contenido.
* Aplicar validaciones de negocio.
* Mantener arquitectura moderna.
* Implementarse en un único archivo Python si es viable.

---

# 2. Stack Tecnológico Final

| Componente             | Tecnología                 |
| ---------------------- | -------------------------- |
| API REST               | FastAPI                    |
| Servidor               | Uvicorn                    |
| ORM                    | SQLAlchemy 2.0             |
| Validación             | Pydantic v2                |
| Base de datos          | SQLite                     |
| IA                     | Azure OpenAI               |
| HTTP Client            | httpx                      |
| Reintentos automáticos | tenacity                   |
| Testing                | pytest                     |
| Variables entorno      | python-dotenv              |
| Documentación          | Swagger/OpenAPI automático |

---

# 3. Arquitectura Recomendada (Archivo Único)

Aunque FastAPI suele estructurarse modularmente, para cumplir el ejercicio se recomienda:

```text
m3_nombre_apellido.py
```

Con organización interna por bloques:

```python
# Imports

# Configuración

# Base de datos

# Modelos SQLAlchemy

# Schemas Pydantic

# Configuración Azure OpenAI

# Servicios IA

# Reglas de negocio

# CRUD helpers

# Endpoints FastAPI

# Inicialización DB

# Main
```

Esto permite:

* mantener archivo único,
* mantener legibilidad,
* facilitar evaluación académica.

---

# 4. Modelo de Datos

## Entidad principal: SocialMediaPost

Basada en el enunciado original. 

## Campos recomendados

| Campo      | Tipo      | Descripción               |
| ---------- | --------- | ------------------------- |
| id         | Integer   | PK                        |
| platform   | String    | LinkedIn, X, Instagram... |
| title      | String    | Tema principal            |
| tone       | String    | Formal, casual, técnico   |
| content    | Text      | Texto generado            |
| hashtags   | Text      | Lista hashtags            |
| link       | String    | URL externa               |
| language   | String    | Idioma                    |
| variants   | JSON/Text | Variantes generadas       |
| created_at | DateTime  | Fecha automática          |
| updated_at | DateTime  | Última actualización      |

---

# 5. Diseño de Generación IA

## Endpoint principal

```http
POST /api/contents/generate
```

## Flujo

### Entrada

```json
{
  "prompt": "IA generativa en educación",
  "platform": "LinkedIn",
  "tone": "Profesional",
  "language": "es",
  "variants": 3
}
```

---

### Proceso

1. Validación entrada
2. Construcción prompt estructurado
3. Llamada Azure OpenAI
4. Reintentos automáticos
5. Validación JSON IA
6. Persistencia SQLite
7. Respuesta API

---

### Salida esperada

```json
{
  "title": "...",
  "platform": "LinkedIn",
  "tone": "Profesional",
  "content": "...",
  "hashtags": ["#IA", "#AI"],
  "variants": [
    "...",
    "...",
    "..."
  ]
}
```

---

# 6. Generación Estructurada JSON

Punto MUY importante.

La IA debe responder SIEMPRE con JSON válido.

## Estrategia recomendada

Usar:

* response_format JSON
* validación Pydantic

## Beneficios

* evita respuestas inconsistentes
* facilita persistencia
* facilita testing
* mejora robustez

---

# 7. Reintentos Automáticos

Implementar con:

Python Software Foundation `tenacity`

## Casos a cubrir

| Error          | Reintentar |
| -------------- | ---------- |
| Timeout        | Sí         |
| 429 Rate limit | Sí         |
| 5xx Azure      | Sí         |
| JSON inválido  | Sí         |

## Estrategia

```python
retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
```

---

# 8. Reglas de Negocio

## Validaciones recomendadas

### Plataforma

Permitir:

* LinkedIn
* X
* Instagram
* Facebook
* TikTok

---

### Longitud

| Plataforma | Regla        |
| ---------- | ------------ |
| X          | <= 280 chars |
| LinkedIn   | <= 3000      |
| Instagram  | <= 2200      |

---

### Hashtags

* máximo 10
* eliminar duplicados

---

### Links

* validación URL
* opcional

---

### Variantes

* mínimo 1
* máximo 5

---

# 9. Endpoints Finales

## CRUD

### Obtener todos

```http
GET /api/contents
```

---

### Obtener por ID

```http
GET /api/contents/{id}
```

---

### Crear manualmente

```http
POST /api/contents
```

---

### Generar con IA

```http
POST /api/contents/generate
```

---

### Actualizar

```http
PUT /api/contents/{id}
```

---

### Eliminar

```http
DELETE /api/contents/{id}
```

---

# 10. Estrategia de Testing

Aunque sea académico, esto sube muchísimo el nivel.

## Testing recomendado

### Unitarios

* validaciones
* schemas
* helpers IA

---

### Integración

* endpoints FastAPI
* SQLite test DB

---

### Mock IA

Mockear Azure OpenAI:

* evitar coste
* evitar dependencia externa

---

## Herramientas

| Tipo      | Herramienta   |
| --------- | ------------- |
| Tests     | pytest        |
| API tests | TestClient    |
| Mock      | unittest.mock |

---

# 11. Diseño Moderno FastAPI

## Buenas prácticas

### Dependency Injection

```python
Depends(get_db)
```

---

### Async/Await

Endpoints async:

```python
async def
```

---

### Tipado completo

```python
def create_post(
    post: SocialMediaPostCreate
)
```

---

### OpenAPI automático

FastAPI generará:

* Swagger UI
* Redoc

Muy útil para evaluación académica.

---

# 12. Flujo Completo del Sistema

```text
Cliente
   ↓
FastAPI Endpoint
   ↓
Validación Pydantic
   ↓
Servicio IA
   ↓
Azure OpenAI
   ↓
JSON estructurado
   ↓
Validación
   ↓
SQLite
   ↓
Respuesta API
```

---

# 13. Configuración Entorno

## Variables `.env`

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_DEPLOYMENT=
DATABASE_URL=sqlite:///socialmedia.db
```

---

# 14. Librerías Necesarias

## requirements.txt recomendado

```txt
fastapi
uvicorn
sqlalchemy
pydantic
httpx
python-dotenv
pytest
tenacity
```

Opcional:

```txt
openai
```

---

# 15. Complejidad Estimada

| Fase               | Tiempo |
| ------------------ | ------ |
| Configuración base | 1h     |
| Modelos + DB       | 1h     |
| CRUD               | 2h     |
| Azure OpenAI       | 2h     |
| Validaciones       | 1h     |
| Testing            | 2h     |
| Ajustes finales    | 1h     |

## Total estimado

### 8–10 horas

---

# 16. Riesgos Técnicos

| Riesgo               | Mitigación                      |
| -------------------- | ------------------------------- |
| JSON inválido IA     | Validación Pydantic             |
| Timeout Azure        | Reintentos                      |
| SQLite locks         | sesiones cortas                 |
| Prompt inconsistente | Prompt engineering estructurado |
| Respuestas largas    | límites por plataforma          |

---

# 17. Recomendación Profesional Final

Para una práctica académica, la mejor relación:

* calidad,
* modernidad,
* simplicidad,
* mantenibilidad

es:

## Arquitectura final recomendada

```text
FastAPI
+ SQLAlchemy 2.0
+ SQLite
+ Azure OpenAI
+ Pydantic v2
+ Testing básico sólido
+ Archivo único organizado
```

---

# 18. Siguiente Paso Recomendado

El siguiente paso lógico sería preparar:

1. Diseño exacto de schemas Pydantic
2. Modelo SQLAlchemy definitivo
3. Contratos JSON IA
4. Prompt engineering
5. Estructura completa del archivo único
6. Estrategia de testing
7. Orden óptimo de implementación

Y después generar:

* el esqueleto completo del proyecto,
* o incluso el archivo final listo para ejecutar.
