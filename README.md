# agent_dev

## Resumen

Este proyecto implementa un filtro de preguntas médicas especializadas usando modelos de lenguaje de Google a través de LangChain. El filtro determina si una pregunta puede ser enviada a un sistema experto, permitiendo solo consultas generales sobre enfermedades neurodegenerativas (principalmente Alzheimer y demencia) y rechazando preguntas de diagnóstico o manejo clínico específico.

## Requisitos

- Docker
- Una clave de API de Google Generative AI (debe colocarse en un archivo `.env` en la raíz del proyecto, por ejemplo: `API_KEY=tu_clave_aqui`).

## Instalación y ejecución

1. **Clona el repositorio y navega a la carpeta del proyecto:**
   ```sh
   git clone <url-del-repositorio>
   cd agent_dev
   ```

2. **Crea un archivo `.env` con tu API Key:**
   ```
   API_KEY=tu_clave_aqui
   ```

3. **Construye la imagen de Docker:**
   ```sh
   docker build -t agent_dev .
   ```

4. **Ejecuta el contenedor:**
   ```sh
   docker run --env-file .env -it agent_dev
   ```

5. **Interactúa con el filtro desde la terminal del contenedor.**

## Estructura principal

- `src/Filter.py`: Script principal del filtro.
- `requirements.txt`: Solo incluye los paquetes estrictamente necesarios.
- `Dockerfile`: Configuración para contenerizar la aplicación.