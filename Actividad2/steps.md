# Memoria del proyecto (guía paso a paso para implementar el chatbot)

## Paso 0 — Validación inicial (antes de tocar código)
**Objetivo:** asegurar que la implementación se hará con tu mismo contexto.

1. Confirmar **estructura** del proyecto: `actividad2/` con `chatbot.py`, `requirements.txt` y informe (md/pdf).
2. Confirmar si el proyecto usará `.env` o variables de entorno para guardar `API Key` y `Endpoint`.
3. Confirmar qué modelo/deployment usarás en Azure (nombre de deployment exacto).

✅ **Tu validación requerida:** “Sí” o cambios.

---

## Paso 1 — Azure OpenAI listo (credenciales + deployment)
**Objetivo:** poder autenticar llamadas desde Python.

1. Crear recurso **Azure OpenAI**.
2. Obtener **API Key** y **Endpoint URL** desde “Keys and Endpoint”.
3. Desplegar un modelo en Azure OpenAI Studio y guardar el **deployment name**.
4. Verificar que el deployment esté activo.

**Entregable del paso:** endpoint, api key y deployment name anotados.

✅ **Tu validación requerida:** confirmación de que tienes esos 3 datos.

---

## Paso 2 — Preparación del entorno Python
**Objetivo:** entorno reproducible.

1. Crear venv:
   - `python -m venv venv`
2. Activar venv (Windows / Linux-Mac).
3. Instalar dependencia:
   - `pip install openai`
4. Generar `requirements.txt`:
   - `pip freeze > requirements.txt`
5. Verificar instalación (import/arranque mínimo).

✅ **Tu validación requerida:** “Instalación OK” y `requirements.txt` generado.

---

## Paso 3 — Diseñar el chatbot (roles + bucle)
**Objetivo:** definir comportamiento antes de programar.

1. Implementar historial de mensajes con roles:
   - `system`: reglas del asistente
   - `user`: mensajes del usuario
   - `assistant`: respuestas del modelo
2. Implementar bucle:
   - mostrar mensaje de bienvenida
   - leer input del usuario
   - si el usuario escribe **"salir"** → finalizar
   - si no, enviar al modelo y mostrar respuesta
3. Definir política de historial para evitar crecimiento indefinido (mínimo viable: historial actual).

✅ **Tu validación requerida:** apruebas el `system prompt` y el criterio de historial.

---

## Paso 4 — Implementar `chatbot.py` con Azure OpenAI
**Objetivo:** que el chatbot funcione end-to-end.

1. Leer `endpoint`, `api_key`, `deployment` (desde `.env`/variables de entorno).
2. Configurar cliente Azure OpenAI.
3. Implementar llamada al modelo usando `messages`.
4. Mostrar respuesta del modelo al usuario.
5. Capturar errores típicos:
   - credenciales incorrectas
   - endpoint inválido
   - fallos de red

✅ **Tu validación requerida:** el chatbot responde correctamente con una prueba manual.

---

## Paso 5 — Parámetros del modelo configurables
**Objetivo:** cumplir requisito de personalización.

1. Añadir parámetros configurables:
   - `temperature`
   - `max_tokens`
   - `top_p`
   - `frequency_penalty`
   - `presence_penalty`
2. Definir valores por defecto.
3. Permitir ajustes (configuración/inicio/argumentos) según se acuerde.

✅ **Tu validación requerida:** confirmas valores por defecto y cómo se ajustan.

---

## Paso 6 — Pruebas: mínimo 3 casos de uso (con evidencias)
**Objetivo:** documentar pruebas y análisis.

Realizar y registrar los 3 casos:
1. **Caso 1:** recomendación de libros (prompt definido por ti)
2. **Caso 2:** respuesta técnica (Python/IA)
3. **Caso 3:** generación creativa (poema infantil u otro, según acuerdo)

Para cada caso:
- ejecutar el chatbot
- capturar evidencia (capturas de terminal)
- anotar parámetros usados
- redactar análisis breve (coherencia, detalle, relevancia, etc.)

✅ **Tu validación requerida:** confirmas evidencias completas de los 3 casos.

---

## Paso 7 — Costes y consumo de tokens + optimización
**Objetivo:** justificar y proponer optimizaciones.

1. Explicar que Azure factura según tokens:
   - tokens de entrada (prompt)
   - tokens de salida (completion)
2. Estimar coste aproximado usando Pricing Calculator (o cálculo equivalente).
3. Relacionar consumo con:
   - respuestas más largas → más tokens
   - historial largo → más tokens
4. Proponer estrategias:
   - limitar `max_tokens`
   - reducir historial
   - resumir conversación
   - usar modelos más económicos para tareas simples
   - cachear respuestas repetidas
   - ajustar `temperature`

✅ **Tu validación requerida:** confirmas que la estimación y propuesta reflejan tus resultados.

---

## Paso 8 — Informe final (PDF mínimo 5 páginas)
**Objetivo:** entregar con formato y contenido requerido.

1. Completar secciones:
   - introducción y objetivos
   - configuración Azure
   - preparación Python
   - desarrollo del chatbot (explicación + código si aplica)
   - pruebas (3 casos + capturas + análisis)
   - costes y optimización
   - conclusiones
2. Revisar formato:
   - Calibri 11
   - interlineado 1,5
   - mínimo 5 páginas
3. Exportar a PDF.

✅ **Tu validación requerida:** revisión final de que el PDF cumple todo.
