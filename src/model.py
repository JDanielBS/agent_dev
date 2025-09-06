# model.py
# Modelo para el chatbot IA

from Filter import MedicalFilter
from ChatbotIA import get_ia_info

class ChatbotIAModel:
    def __init__(self, filter_prompt):
        self.filtro = MedicalFilter(filter_prompt_template=filter_prompt)

    def procesar_pregunta(self, pregunta: str):
        ok, msg = self.filtro.filter_question(pregunta)
        if ok:
            respuesta = get_ia_info(pregunta)
            return respuesta
        else:
            return msg
