# Actividad 2 - Chatbot Azure OpenAI

Este proyecto implementa un chatbot en Python usando Azure OpenAI.

## Configuración
Se utilizará un archivo `.env` en la carpeta `actividad2/` con:
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_DEPLOYMENT

Ejemplo de `.env`:
```dotenv
AZURE_OPENAI_ENDPOINT=https://TU-RECURSO.openai.azure.com
AZURE_OPENAI_API_KEY=TU_API_KEY
AZURE_OPENAI_DEPLOYMENT=gpt-5.4-nano

# Opcional (si no lo pones, se usa por defecto):
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Parámetros opcionales del modelo (opcional):
TEMPERATURE=0.7
MAX_TOKENS=800
TOP_P=1
FREQUENCY_PENALTY=0
PRESENCE_PENALTY=0
```

## Ejecución
...
