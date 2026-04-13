import sys
import os
import requests
import functions_framework
from flask import jsonify

# Modificar sys.path para poder importar módulos compartidos cuando se ejecute de forma remota en GCP o de forma local.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Importamos el cliente de Supabase desde nuestra carpeta 'shared' (ubicada en la base del repo)
from shared.supabase_client import get_supabase_client

@functions_framework.http
def ejecutar_agente_macro(request):
    """
    Entrypoint para HTTP Cloud Function.
    Hace una petición GET a una API pública, extrae un dato y lo formatea en JSON.
    Está lista para interactuar con la Base de Datos vía el cliente Supabase centralizado.
    """
    try:
        # 1. Petición HTTP a una API pública.
        # Sirve para extraer la materia prima que luego consumirá tu LLM.
        # Aquí usamos JSONPlaceholder como caso de ejemplo puro:
        api_url = "https://jsonplaceholder.typicode.com/posts/1"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code != 200:
            return jsonify({
                "error": "Error al consultar la API externa",
                "status_code": response.status_code
            }), 502

        data = response.json()

        # 2. Procesamiento del dato (El pipeline lógico)
        # Extraemos algo específico que interese analizar en el ecosistema (por ej. un ticker o un post).
        resultado_procesado = {
            "agente": "Agente Macro",
            "dato_extraido": data.get("title", "Sin titulo"),
            "fuente": api_url,
            "status": "success"
        }

        # 3. (Condicional) Escritura/Lectura en Supabase
        # Descomenta este bloque para guardar el resultado en tu esquema de BD real 
        # (Asegúrate de configurar SUPABASE_URL y SUPABASE_KEY en el ambiente local/GCP)
        """
        supabase = get_supabase_client()
        if supabase:
            insert_response = (
                supabase.table("tus_datos_macro")
                .insert({"valor": resultado_procesado})
                .execute()
            )
            resultado_procesado["supabase_id"] = insert_response.data[0]["id"]
        """

        # Retornar el JSON validado y estructurado al agente orquestador (n8n).
        return jsonify(resultado_procesado), 200

    except Exception as e:
        # Registro básico de errores para revisar en Google Cloud Platform Logs Explorer
        print(f"Error drástico en agente macro: {e}")
        return jsonify({"error": str(e)}), 500
