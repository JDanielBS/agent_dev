import os
from dotenv import load_dotenv
from Filter import MedicalFilter
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

def get_ia_info(question: str):
    """
    Responde preguntas generales sobre Inteligencia Artificial.
    """
    ia_prompt = PromptTemplate(
        input_variables=["user_input"],
        template=(
            "Eres un chatbot experto en Inteligencia Artificial. "
            "Responde de forma clara, concisa y educativa a la siguiente pregunta sobre IA: {user_input}"
        )
    )
    llm = GoogleGenerativeAI(model="gemma-3-27b-it", api_key=os.getenv("API_KEY"))
    pipeline = ia_prompt | llm | StrOutputParser()
    return pipeline.invoke({"user_input": question}).strip()

if __name__ == "__main__":
    ia_filter_prompt = (
        "Eres un filtro de contenido especializado en Inteligencia Artificial.\n"
        "Tu tarea es recibir preguntas de los usuarios y decidir si pueden ser respondidas por un chatbot experto en IA.\n\n"
        "Solo aceptas preguntas relacionadas con conceptos, historia, aplicaciones, algoritmos, ética, avances, riesgos, oportunidades, funcionamiento, tipos y ejemplos de Inteligencia Artificial.\n"
        "No aceptas preguntas sobre temas médicos, diagnósticos, enfermedades, síntomas, tratamientos, ni consultas personales de salud.\n\n"
        "Si la pregunta del usuario trata sobre Inteligencia Artificial, responde exactamente con: 'YES'.\n"
        "Si la pregunta no es sobre IA, responde con: 'NO'. Además, añade: 'Lo siento, solo puedo responder preguntas relacionadas con Inteligencia Artificial.'\n\n"
        "Pregunta del usuario: {user_input}"
    )
    filtro = MedicalFilter(filter_prompt_template=ia_filter_prompt)
    print("Chatbot IA: ¡Hola! Solo puedo responder preguntas sobre Inteligencia Artificial. ¡Pregúntame lo que quieras sobre IA!")
    while True:
        user_input = input("\nUsuario: ")
        if user_input.lower() in ["salir", "adiós"]:
            print("Chatbot IA: ¡Hasta luego!")
            break
        # Filtrar si es pregunta de IA
        ok, msg = filtro.filter_question(user_input)
        if ok:
            respuesta = get_ia_info(user_input)
            print(f"\nChatbot IA: {respuesta}")
        else:
            print(f"\nChatbot IA: {msg}")
