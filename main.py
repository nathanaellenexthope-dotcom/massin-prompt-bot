#!/usr/bin/env python3
import sys
import os
from datetime import datetime

from src.scraper import MassInScraper
from src.prompt_generator import PromptGenerator
from src.sheets_manager import SheetsManager

def send_discord_notification(webhook_url, message):
    import requests
    payload = {
        "content": message,
        "username": "Prompt Generator Bot"
    }
    try:
        requests.post(webhook_url, json=payload, timeout=10)
    except Exception as e:
        print(f"Erreur notification Discord: {e}")

def main():
    product_name = os.environ.get('PRODUCT_NAME', '').strip()
    
    if not product_name:
        if len(sys.argv) > 1:
            product_name = sys.argv[1]
        else:
            print("Erreur: Aucun produit specifie. Definir PRODUCT_NAME.")
            sys.exit(1)
    
    print(f"Demarrage du workflow pour: '{product_name}'")
    
    scraper = MassInScraper()
    prompt_gen = PromptGenerator()
    
    spreadsheet_id = os.environ.get('GOOGLE_SHEET_ID')
    credentials_path = os.environ.get('GOOGLE_CREDENTIALS_PATH', 'google_credentials.json')
    
    if not spreadsheet_id:
        print("Erreur: GOOGLE_SHEET_ID non defini.")
        sys.exit(1)
    
    sheets = SheetsManager(spreadsheet_id, credentials_path)
    
    sheet_name = datetime.now().strftime('%Y-%m-%d')
    worksheet = sheets.create_or_get_sheet(sheet_name)
    
    print(f"Recherche du produit: {product_name}")
    
    product_info = scraper.search_product(product_name)
    
    if product_info:
        print(f"Produit trouve: {product_info['name']}")
        prompt = prompt_gen.generate_prompt(product_info)
        
        sheets.add_product(
            worksheet,
            product_info['name'],
            product_info['image_url'],
            prompt
        )
        
        status = "Succes"
        image_url = product_info['image_url']
    else:
        print(f"Produit non trouve: {product_name}")
        status = "Non trouve"
        image_url = ""
    
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        sheet_url = sheets.get_sheet_url(worksheet)
        
        emoji = "✅" if status == "Succes" else "❌"
        message = (
            f"Workflow termine !\n\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Produit: {product_name}\n"
            f"Statut: {emoji} {status}\n"
            f"Google Sheet: {sheet_url}"
        )
        
        send_discord_notification(webhook_url, message)
        print("Notification Discord envoyee.")
    
    print(f"Workflow termine !")
    print(f"Sheet: {sheets.get_sheet_url(worksheet)}")

if __name__ == '__main__':
    main()
