# Planificación - Actividad 2: Implementación de un chatbot inteligente con Azure OpenAI

## 1. Información general

**Actividad:** Implementación de un chatbot inteligente con Azure OpenAI  
**Archivo principal a desarrollar:** `chatbot.py`  
**Formato de entrega final:** PDF (mínimo 5 páginas)  
**Objetivo principal:** Construir un chatbot funcional en Python conectado a Azure OpenAI y documentar pruebas, costes y optimización.

---

## 2. Objetivos de la actividad

- Implementar un chatbot funcional utilizando Azure OpenAI.
- Configurar un entorno Python correctamente.
- Conectar una aplicación local con un servicio cloud (Azure OpenAI).
- Personalizar parámetros del modelo (`temperature`, `max_tokens`, `top_p`, etc.).
- Probar el chatbot con al menos 3 casos de uso.
- Analizar consumo de tokens y proponer estrategias de optimización de costes.

---

## 3. Requisitos del chatbot

El chatbot debe cumplir:

- Configuración con **endpoint** y **API key** de Azure OpenAI.
- Bucle de conversación con entrada del usuario.
- Respuesta basada en el modelo configurado.
- Finalización al escribir: **"salir"**.
- Uso de roles en mensajes:
  - `system`
  - `user`
  - `assistant`

---

## 4. Fases de trabajo

---

### Fase 1: Configuración en Azure (Duración estimada: 1-2 horas)

#### Tareas
- [ ] Acceder al portal de Azure.
- [ ] Crear recurso **Azure OpenAI**.
- [ ] Obtener:
  - [ ] API Key
  - [ ] Endpoint
- [ ] Desplegar un modelo (ejemplo: GPT-3.5-turbo o GPT-4).
- [ ] Guardar el nombre del deployment.

#### Entregables
- Credenciales verificadas (API Key y endpoint).
- Deployment configurado y activo.

---

### Fase 2: Preparación del entorno local (Duración estimada: 30-60 min)

#### Tareas
- [ ] Instalar Python.
- [ ] Instalar Visual Studio Code.
- [ ] Crear entorno virtual:

```bash
python -m venv venv
````

* [ ] Activar entorno virtual:

  * Windows:

    ```bash
    venv\Scripts\activate
    ```
  * Linux/Mac:

    ```bash
    source venv/bin/activate
    ```

* [ ] Instalar librería OpenAI:

```bash
pip install openai
```

* [ ] Crear estructura de proyecto recomendada:

```
actividad2/
│── chatbot.py
│── requirements.txt
│── planificacion_actividad2.md
│── informe.pdf
```

* [ ] Exportar dependencias:

```bash
pip freeze > requirements.txt
```

#### Entregables

* Proyecto listo y dependencias instaladas.
* Entorno virtual funcional.

---

### Fase 3: Desarrollo del chatbot (Duración estimada: 2-4 horas)

#### Tareas principales

* [ ] Crear archivo `chatbot.py`.

* [ ] Configurar conexión a Azure OpenAI con:

  * endpoint
  * api_key
  * deployment/model

* [ ] Crear estructura básica del bucle conversacional:

  * Mostrar mensaje de bienvenida.
  * Leer input del usuario.
  * Si el usuario escribe "salir" -> finalizar.
  * Enviar conversación al modelo y mostrar respuesta.

* [ ] Implementar roles:

  * `system`: define comportamiento del bot
  * `user`: mensajes del usuario
  * `assistant`: respuestas del modelo

* [ ] Añadir personalización de parámetros:

  * `temperature`
  * `max_tokens`
  * `top_p`
  * `frequency_penalty`
  * `presence_penalty`

#### Checklist de calidad del código

* [ ] Código ejecuta sin errores.
* [ ] Captura excepciones (errores de red, credenciales incorrectas, etc.).
* [ ] Código comentado y claro.
* [ ] Variables sensibles no están hardcodeadas (recomendado usar `.env`).

#### Entregables

* `chatbot.py` funcional.
* Conversación fluida con salida por "salir".

---

### Fase 4: Pruebas del chatbot (Duración estimada: 1-2 horas)

#### Requisito obligatorio

Documentar **mínimo 3 casos de uso** con capturas de pantalla y análisis.

#### Casos de uso sugeridos

* [ ] Caso 1: Curiosidades de física a nivel divulgativo
* [ ] Caso 2: Respuestas técnicas programación en c++
* [ ] Caso 3: Generación breve poema infantil

#### Tareas

* [ ] Ejecutar chatbot varias veces con parámetros distintos.
* [ ] Guardar evidencias (capturas o logs).
* [ ] Comparar impacto de:

  * temperature alta vs baja
  * max_tokens corto vs largo

#### Entregables

* Evidencia de pruebas (capturas).
* Análisis escrito de los resultados.

---

### Fase 5: Optimización y análisis de costes (Duración estimada: 1-2 horas)

#### Tareas

* [ ] Consultar Azure Pricing Calculator.
* [ ] Estimar coste aproximado por interacción.
* [ ] Identificar consumo de tokens aproximado en pruebas.

#### Estrategias de optimización a proponer

* [ ] Reducir `max_tokens`.
* [ ] Resumir conversación y no enviar historial completo.
* [ ] Limitar longitud del input del usuario.
* [ ] Cachear respuestas repetidas.
* [ ] Usar modelos más baratos para tareas simples.
* [ ] Ajustar `temperature` y `top_p` según el objetivo.

#### Entregables

* Estimación de coste.
* Propuesta de optimización documentada.

---

### Fase 6: Elaboración del informe final (Duración estimada: 3-6 horas)

#### Requisitos de formato

* Mínimo 5 páginas.
* Fuente Calibri tamaño 11.
* Interlineado 1,5.
* Entrega en PDF.

#### Estructura recomendada del informe

1. Portada (nombre, apellidos, fecha, actividad)
2. Introducción y objetivos
3. Configuración del entorno Azure
4. Preparación del entorno Python
5. Desarrollo del chatbot (explicación del código)
6. Pruebas (3 casos con capturas y análisis)
7. Costes y optimización
8. Conclusión

#### Checklist final del informe

* [ ] Cumple mínimo 5 páginas.
* [ ] Incluye capturas de pantalla.
* [ ] Incluye explicación de parámetros.
* [ ] Incluye apartado de costes.
* [ ] Incluye propuestas de optimización.
* [ ] PDF correctamente exportado.

#### Entregables

* `informe.pdf`

---

## 5. Planificación temporal sugerida

| Fase                  | Duración estimada | Resultado                   |
| --------------------- | ----------------- | --------------------------- |
| Configuración Azure   | 1-2 h             | Endpoint + API key + modelo |
| Entorno Python        | 0.5-1 h           | Proyecto preparado          |
| Desarrollo chatbot    | 2-4 h             | chatbot.py funcional        |
| Pruebas               | 1-2 h             | 3 casos documentados        |
| Costes y optimización | 1-2 h             | estimación + estrategias    |
| Informe PDF           | 3-6 h             | documento final             |

---

## 6. Validación según rúbrica

### Configuración correcta del entorno (10%)

* [ ] Azure configurado correctamente
* [ ] Claves API obtenidas y probadas

### Implementación técnica del chatbot (20%)

* [ ] Código funcional
* [ ] Parámetros configurables (temperature, max_tokens, top_p)

### Documentación de pruebas (20%)

* [ ] Tres escenarios distintos
* [ ] Capturas y análisis

### Optimización de recursos (20%)

* [ ] Estimación de costes
* [ ] Propuestas claras de optimización

### Formato y claridad (30%)

* [ ] Informe mínimo 5 páginas
* [ ] Formato correcto (Calibri 11, 1.5)
* [ ] Redacción clara y ordenada

---

## 7. Entregables finales

* [ ] `chatbot.py`
* [ ] `requirements.txt`
* [ ] `informe.pdf`

---

## 8. Notas técnicas recomendadas

* Usar variables de entorno para proteger credenciales.
* Mantener un historial limitado de mensajes para ahorrar tokens.
* Ajustar `max_tokens` según tipo de respuesta esperada.
* Definir un `system prompt` claro para guiar el comportamiento del bot.

---

