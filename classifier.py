import os
import json
from groq import Groq

def classify_lead(text):
    """
    Sends the extracted text to Llama 3 on Groq to classify it and generate a sales pitch.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    client = Groq(api_key=api_key)
    
    system_prompt = """
    Eres un Senior Sales Engineer y experto en IA. 
    Tu objetivo es analizar el contenido de una empresa para determinar si necesitan servicios de Desarrollo Web o Inteligencia Artificial.
    
    Responde ÚNICAMENTE en formato JSON con los siguientes campos:
    {
        "company_name": "Nombre de la empresa",
        "needs_ai": "Booleano (true/false)",
        "priority_score": "Entero del 1 al 10",
        "technical_reason": "Breve explicación técnica de por qué necesitan estos servicios",
        "custom_pitch": "Un mensaje persuasivo personalizado para venderles servicios de AmauryDev (Web/IA) vía WhatsApp o Email"
    }
    """

    user_content = f"Analiza el siguiente texto extraído de la web de una empresa:\n\n{text[:5000]}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"}
        )

        response_text = chat_completion.choices[0].message.content
        return json.loads(response_text)

    except Exception as e:
        print(f"Error classifying lead: {e}")
        return None
