# view.py
# Vista para el chatbot IA (Tkinter)

import tkinter as tk
from tkinter import scrolledtext

class ChatbotIAView:
    def __init__(self, root):
        self.root = root
        self.on_send_callback = None
        self.configure_view()

    def configure_view(self):
        self.root.title("Chatbot IA - Pregunta sobre Inteligencia Artificial")
        self.root.geometry("700x550")
        self.root.minsize(500, 400)

        # Frame principal para el chat
        self.chat_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Área de mensajes (canvas + frame para alineación)
        self.canvas = tk.Canvas(self.chat_frame, bg="#f5f5f5", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.messages_frame = tk.Frame(self.canvas, bg="#f5f5f5")
        self.messages_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Campo de entrada (Text widget para multilinea, ovalado)
        self.input_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0,10))

        self.entry = tk.Text(self.input_frame, height=2, font=("Arial", 12), wrap=tk.WORD, bd=0, relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5), pady=5, ipady=6)
        self.entry.bind('<Return>', self._on_return)
        self.entry.bind('<Shift-Return>', self._shift_enter)
        self.entry.bind('<KeyRelease>', self._limit_lines)

        # Ovalado visual (simulado con un Frame y color de fondo)
        self.entry.config(bg="#ffffff", highlightbackground="#cccccc", highlightcolor="#cccccc", highlightthickness=1)
        self.entry.config(borderwidth=0)
        self.entry.config(insertbackground="#333333")

        # Botón enviar
        self.send_button = tk.Button(self.input_frame, text="Enviar", command=self.on_send, font=("Arial", 12), bg="#4a90e2", fg="white", relief=tk.FLAT, padx=16, pady=4)
        self.send_button.pack(side=tk.RIGHT, padx=(5,0), pady=5)

        # Mensaje de bienvenida
        self.mostrar_mensaje("Chatbot IA", "¡Hola! Solo puedo responder preguntas sobre Inteligencia Artificial. ¡Pregúntame lo que quieras sobre IA!", align="left")

    def set_on_send(self, callback):
        self.on_send_callback = callback

    def _on_return(self, event):
        # Enviar mensaje con Enter, agregar nueva línea solo con Shift+Enter
        self.on_send()
        return "break"

    def _shift_enter(self, event):
        self.entry.insert(tk.INSERT, '\n')
        return "break"

    def _limit_lines(self, event=None):
        # Limitar a 2 líneas visibles, permitir scroll si hay más
        lines = int(self.entry.index('end-1c').split('.')[0])
        if lines > 2:
            self.entry.config(height=2, yscrollcommand=None)
            self.entry.yview_moveto(1.0)
        else:
            self.entry.config(height=2)

    def on_send(self):
        pregunta = self.entry.get("1.0", tk.END).strip()
        if pregunta and self.on_send_callback:
            self.entry.delete("1.0", tk.END)
            self.on_send_callback(pregunta)

    def mostrar_respuesta(self, pregunta, respuesta):
        self.mostrar_mensaje("Tú", pregunta, align="right")
        self.mostrar_mensaje("Chatbot IA", self.formatear_respuesta(respuesta), align="left")

    def mostrar_mensaje(self, remitente, texto, align="left"):
        # Widget de mensaje tipo burbuja
        frame = tk.Frame(self.messages_frame, bg="#f5f5f5")
        color = "#e1f0ff" if remitente == "Chatbot IA" else "#d1ffd6"
        anchor = "w" if align == "left" else "e"
        padx = (10, 60) if align == "left" else (60, 10)
        label = tk.Label(frame, text=f"{remitente}: {texto}", bg=color, fg="#222", font=("Arial", 12), wraplength=420, justify="left" if align=="left" else "right", padx=10, pady=6, bd=0, relief=tk.FLAT)
        label.pack(anchor=anchor, fill=tk.NONE)
        frame.pack(anchor=anchor, fill=tk.X, padx=padx, pady=3)
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))

    def formatear_respuesta(self, respuesta):
        # Quitar markdown simple como **negrita** o *cursiva*
        import re
        respuesta = re.sub(r'\*\*(.*?)\*\*', r'\1', respuesta)
        respuesta = re.sub(r'\*(.*?)\*', r'\1', respuesta)
        respuesta = re.sub(r'__(.*?)__', r'\1', respuesta)
        respuesta = re.sub(r'_(.*?)_', r'\1', respuesta)
        return respuesta
