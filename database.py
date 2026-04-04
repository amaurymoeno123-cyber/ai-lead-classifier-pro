import os
from supabase import create_client, Client

def save_to_supabase(data):
    """
    Simulates or saves lead data to Supabase table.
    Expects data as a dictionary with specific fields.
    """
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("Supabase credentials not found. Skipping database insertion (Mock Mode).")
        return None

    try:
        supabase: Client = create_client(url, key)
        response = supabase.table("leads").insert(data).execute()
        return response.data
    except Exception as e:
        print(f"Error saving to Supabase: {e}")
        return None
