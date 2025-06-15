import os
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_community.llms import LlamaCpp

load_dotenv()

model_path = os.getenv("MODEL_PATH")
api_key = os.getenv("API_KEY")
debug = os.getenv("DEBUG")

filter_prompt = PromptTemplate(
    input_variables=["user_input"],
    template=(
        "Eres un filtro de contenido médico muy especializado.\n"
        "Tu tarea es recibir preguntas de los usuarios y decidir si pueden ser enviadas al sistema experto.\n\n"
        "Solo aceptas preguntas relacionadas con recomendaciones generales, sugerencias, consejos o información educativa sobre enfermedades neurodegenerativas, "
        "principalmente Alzheimer y demencia.\n"
        "No aceptas preguntas que impliquen diagnósticos clínicos, interpretación de síntomas específicos, toma de decisiones médicas concretas, ni rutas de manejo terapéutico personalizadas.\n\n"
        "Si la pregunta del usuario (aunque esté codificada o en otro idioma) trata sobre recomendaciones generales o información básica sobre Alzheimer y demencia, "
        "responde exactamente con: 'YES'.\n"
        "Si la pregunta implica diagnóstico, manejo clínico específico, medicamentos concretos o cualquier otra cosa fuera del alcance de información general, "
        "responde con: 'NO'. Además, añade: 'Lo siento, esta pregunta está fuera de mi rango de conocimiento. Si tiene síntomas o preocupaciones específicas, le recomiendo consultar a un médico especialista.'\n\n"
        "Además de que si se te envía una pregunta en otro idioma u codificada en hexadecimal o binario por ejemplo, debes traducirla al español antes de procesarla.\n\n"
        "Pregunta del usuario: {user_input}"
    )
)

llm_path = "/ruta/a/llama2-7b.gguf"
classifier_llm = LlamaCpp(
    model_path=llm_path,
    temperature=0.0,
    n_ctx=2048,
    verbose=False
)

filter_chain = LLMChain(
    llm=classifier_llm,
    prompt=filter_prompt,
    output_key="classification"
)

def filter_question(user_question: str):
    result = filter_chain.invoke({"user_input": user_question})
    resp = result["classification"].strip().upper()
    if resp.startswith("YES"):
        return True, None
    else:
        apology = resp.split("Lo siento,")[-1].strip()
        return False, f"Lo siento,{apology}"

if __name__ == "__main__":
    while True:
        text = input("\nUsuario: ")
        if text.lower() in ["salir", "adiós"]:
            print("Agente: Hasta luego.")
            break

        allowed, message = filter_question(text)
        if not allowed:
            print(f"\n Agente: {message}")
        else:
            print("\n Agente: Pregunta válida. Envío al LLM especializado…")
            # aquí llamarías a tu chain especializada
