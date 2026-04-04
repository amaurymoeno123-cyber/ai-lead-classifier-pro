# 🤖 AI Lead Classifier for AmauryDev

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Llama 3](https://img.shields.io/badge/LLM-Llama_3-orange.svg)](https://groq.com/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-green.svg)](https://supabase.com/)

El **AI Lead Classifier** es el núcleo de automatización de ventas para **AmauryDev**. Este script extrae información estratégica de cualquier URL, la analiza mediante Inteligencia Artificial (Llama 3) y determina si la empresa es un cliente potencial para servicios de IA o Desarrollo Web, generando incluso un **Sales Pitch** personalizado.

## 🌟 Características Principales

- **Scraping Selectivo**: Solo extrae contenido relevante (h1-h3, p) para optimizar tokens y precisión.
- **Análisis con Llama 3 (Groq)**: Clasificación ultrarrápida y precisa de leads.
- **Persistencia en Supabase**: Guarda automáticamente los resultados en la nube.
- **Modo Demo (Mock Mode)**: Ejecuta el script sin necesidad de claves API para pruebas rápidas.
- **Sales Pitch Generativo**: La IA redacta un mensaje listo para enviar por WhatsApp o Email.

## 🛠️ Requisitos e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/ai-lead-classifier.git
    cd ai-lead-classifier
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar Variables de Entorno:**
    Renombra el archivo `.env.example` a `.env` y añade tus credenciales de Groq y Supabase.
    ```bash
    cp .env.example .env
    ```

## 🗄️ Configuración de Base de Datos (Supabase)

Para inicializar tu base de datos, ejecuta el siguiente comando SQL en el Editor SQL de tu panel de Supabase:

```sql
-- Crear tabla para AI Leads
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    needs_ai BOOLEAN,
    priority_score INTEGER CHECK (priority_score >= 1 AND priority_score <= 10),
    technical_reason TEXT,
    custom_pitch TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
```

## 🚀 Uso del Script

### Dashboard Web (Moderno)
Para una experiencia premium con interfaz visual:
```bash
streamlit run streamlit_app.py
```

### Ejecución CLI (Estándar)
Por defecto, analizará `amaurydev.com`:
```bash
python main.py
```

### Analizar una URL Específica via CLI
```bash
python main.py --url https://ejemplo.com
```

### 💡 Modo Demo (Mock Mode)
Si no configuras las API Keys en el `.env`, el script entrará automáticamente en **Modo Demo**. Esto permite ver el flujo del programa con datos de prueba realistas sin necesidad de configurar nada.

## 📁 Estructura del Proyecto
- `main.py`: Orquestador principal y lógica de Mock Mode.
- `scraper.py`: Extracción de texto refinada con BeautifulSoup4.
- `classifier.py`: Integración con Groq (Llama 3).
- `database.py`: Gestión de inserciones en Supabase.
- `schema.sql`: Estructura de la base de datos.

---
Hecho con ⚡ por [AmauryDev](https://amaurydev.com)
