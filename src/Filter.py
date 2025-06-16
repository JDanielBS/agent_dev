import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Función para crear una chain dinámica según modelo
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

# Cadena para el modelo
llm = GoogleGenerativeAI(model="gemma-3-27b-it", api_key=os.getenv("API_KEY"))

pipeline = filter_prompt | llm | StrOutputParser()

def filter_question(q: str):
    resp = pipeline.invoke({"user_input": q}).strip()
    if resp.upper().startswith("YES"):
        return True, None
    else:
        apology = resp.split("Lo siento, ")[-1].strip()
        return False, f"Lo siento,{apology}"

if __name__ == "__main__":
    while True:
        text = input("\nUsuario: ")
        if text.lower() in ["salir", "adiós"]:
            print("Agente: Hasta luego.")
            break

        ok, msg = filter_question(text)

        if not ok:
            print(f"\n Agente: {msg}")
        else:
            print("\n Agente: Pregunta válida. Envío al LLM especializado…")
            # aquí llamarías a tu chain especializada
