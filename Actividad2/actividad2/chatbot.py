# chatbot.py
import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import AzureOpenAI


def load_config() -> Dict[str, str]:
    """Load Azure OpenAI configuration from environment (via .env)."""
    # Carga .env desde el directorio actual (actividad2/)
    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not endpoint or not api_key or not deployment:
        raise RuntimeError(
            "Faltan variables de entorno. Asegúrate de tener en .env: "
            "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT"
        )

    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "deployment": deployment,
    }


def build_system_prompt() -> str:
    # Spanish, tono natural; con capacidad de adaptar a técnico/coloquial.
    return (
        "Eres un asistente conversacional en español. "
        "Hablas de forma clara y natural (no excesivamente formal). "
        "Cuando el usuario haga preguntas técnicas (programación, IA, APIs, etc.), "
        "responde con más detalle y precisión técnica. "
        "Cuando el usuario busque algo casual (curiosidades, opiniones, consejos generales), "
        "responde con un tono más coloquial y cercano. "
        "Si el usuario mezcla ambos, equilibra y pregunta aclaraciones cuando haga falta."
    )


def create_client(endpoint: str, api_key: str) -> AzureOpenAI:
    # En Azure, api_version debe ser válida para tu recurso/deployment.
    # Si el valor falla, suele verse como 404 (resource not found).
    api_version = os.getenv("AZURE_OPENAI_API_VERSION") or "2024-02-15-preview"

    # Normaliza endpoint por seguridad (quitamos espacios y dejamos sin doble '//' al final)
    endpoint = endpoint.strip()

    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )


def run_chat() -> None:
    config = load_config()
    client = create_client(config["endpoint"], config["api_key"])
    deployment = config["deployment"]

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": build_system_prompt()},
    ]

    print("Chatbot listo. Escribe 'salir' para terminar.\n")

    while True:
        user_text = input("Tú: ").strip()
        if not user_text:
            continue
        if user_text.lower() == "salir":
            print("Hasta luego!")
            return

        messages.append({"role": "user", "content": user_text})

        # Historial mínimo viable: nos quedamos con system + últimos turnos
        # Ajustable: 4 turnos completos (user+assistant).
        max_turns = 4
        system_msg = messages[0]
        trimmed = [system_msg]
        history = messages[1:]
        # history contains user/assistant alternating; recortamos desde el final
        if len(history) > (max_turns * 2):
            history = history[-(max_turns * 2) :]
        trimmed.extend(history)
        messages = trimmed

        try:
            completion = client.chat.completions.create(
                model=deployment,
                messages=messages,
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                # Este modelo no soporta max_tokens; usar max_completion_tokens
                max_completion_tokens=int(
                    os.getenv("MAX_COMPLETION_TOKENS")
                    or os.getenv("MAX_TOKENS", "800")
                ),
                top_p=float(os.getenv("TOP_P", "1")),
                frequency_penalty=float(os.getenv("FREQUENCY_PENALTY", "0")),
                presence_penalty=float(os.getenv("PRESENCE_PENALTY", "0")),
            )
            assistant_text = completion.choices[0].message.content or ""
            print(f"Asistente: {assistant_text}\n")
            messages.append({"role": "assistant", "content": assistant_text})
        except Exception as e:
            print("Error al comunicarse con Azure OpenAI:", str(e))
            print("Revisa endpoint/key/deployment y tu conectividad.\n")


if __name__ == "__main__":
    run_chat()
