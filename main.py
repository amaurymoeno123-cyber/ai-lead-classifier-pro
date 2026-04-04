import os
import argparse
from dotenv import load_dotenv
from scraper import extract_info
from classifier import classify_lead
from database import save_to_supabase

# Load environment variables
load_dotenv()

def run_lead_classification(url):
    """
    Main orchestration function for AI Lead Classifier.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    # MOCK MODE check
    is_mock = not groq_api_key or not supabase_url or not supabase_key

    if is_mock:
        print("\n[INFO] No API Keys found. Running in DEMO MODE with sample data...\n")
        # Simulating process with hardcoded data for demonstration
        mock_data = {
            "company_name": "AmauryDev Sample",
            "needs_ai": True,
            "priority_score": 9,
            "technical_reason": "Based on the content of your site, adding an AI lead classifier would optimize sales processes.",
            "custom_pitch": "Hola! He analizado tu web. Con IA de AmauryDev podrías automatizar la captación de leads un 40% mejor. ¿Hablamos?"
        }
        print(f"--- MOCK RESULT ---")
        print(f"Company: {mock_data['company_name']}")
        print(f"Priority: {mock_data['priority_score']}/10")
        print(f"Pitch: {mock_data['custom_pitch']}")
        print("-------------------\n")
        return mock_data

    # PRODUCTION MODE
    print(f"[INFO] Processing URL: {url}")
    
    # 1. Scrape
    text = extract_info(url)
    if not text:
        print("[ERROR] Could not extract information from the URL.")
        return None
    
    # 2. Classify
    print("[AI] Classifying lead using Llama 3 (Groq)...")
    classification = classify_lead(text)
    if not classification:
        print("[ERROR] AI Classification failed.")
        return None
    
    # 3. Save
    print("[DB] Saving results to Supabase...")
    saved_data = save_to_supabase(classification)
    
    if saved_data:
        print("[SUCCESS] Lead data saved.")
    else:
        print("[WARNING] Could not save lead to database.")
    
    # Final Summary
    print("\n--- CLASSIFICATION RESULT ---")
    for key, value in classification.items():
        print(f"{key.replace('_', ' ').capitalize()}: {value}")
    print("-----------------------------\n")
    
    return classification

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Lead Classifier for AmauryDev")
    parser.add_argument("--url", type=str, help="The URL of the company to analyze", default="https://amaurydev.com")
    args = parser.parse_args()

    run_lead_classification(args.url)
