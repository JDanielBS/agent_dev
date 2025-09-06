# controller.py
# Controlador para el chatbot IA

import tkinter as tk
from model import ChatbotIAModel
from view import ChatbotIAView

IA_FILTER_PROMPT = (
    "Eres un filtro de contenido especializado en Inteligencia Artificial.\n"
    "Tu tarea es recibir preguntas de los usuarios y decidir si pueden ser respondidas por un chatbot experto en IA.\n\n"
    "Solo aceptas preguntas relacionadas con conceptos, historia, aplicaciones, algoritmos, ética, avances, riesgos, oportunidades, funcionamiento, tipos y ejemplos de Inteligencia Artificial.\n"
    "No aceptas preguntas sobre temas médicos, diagnósticos, enfermedades, síntomas, tratamientos, ni consultas personales de salud.\n\n"
    "Si la pregunta del usuario trata sobre Inteligencia Artificial, responde exactamente con: 'YES'.\n"
    "Si la pregunta no es sobre IA, responde con: 'NO'. Además, añade: 'Lo siento, solo puedo responder preguntas relacionadas con Inteligencia Artificial.'\n\n"
    "Pregunta del usuario: {user_input}"
)

class ChatbotIAController:
    def __init__(self, root):
        self.model = ChatbotIAModel(IA_FILTER_PROMPT)
        self.view = ChatbotIAView(root)
        self.view.set_on_send(self.procesar_pregunta)

    def procesar_pregunta(self, pregunta):
        respuesta = self.model.procesar_pregunta(pregunta)
        self.view.mostrar_respuesta(pregunta, respuesta)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotIAController(root)
    root.mainloop()
