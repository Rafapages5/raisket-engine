import os
from supabase import create_client, Client

# Se intenta mantener un cliente referenciado centralmente en el entorno en vivo
# Para mitigar reconstrucciones constantes y agotamiento del pool de conexiones.
_supabase_client = None

def get_supabase_client() -> Client:
    """
    Inicializa (si no existe) y retorna el cliente de Supabase de manera segura.
    Utiliza el entorno que ya haya sido cargado o inyectado en Cloud Run / Cloud Functions.
    Nunca define las credenciales aquí directamente.
    """
    global _supabase_client
    
    if _supabase_client is not None:
        return _supabase_client

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        print("ADVERTENCIA (raisket-engine): SUPABASE_URL o SUPABASE_KEY no definidos en entorno.")
        return None

    try:
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as e:
        print(f"Error al inicializar el cliente Python de Supabase: {e}")
        return None
