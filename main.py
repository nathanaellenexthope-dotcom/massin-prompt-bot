#!/usr/bin/env python3
import sys
import os
from datetime import datetime

from src.scraper import ProductScraper
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
    if len(sys.argv) > 1:
        product_names = sys.argv[1:]
    elif os.environ.get('PRODUCTS'):
        product_names = [p.strip() for p in os.environ.get('PRODUCTS').split(',')]
    else:
        print("Erreur: Aucun produit specifie.")
        print("Usage: python main.py 'nom produit 1' 'nom produit 2'")
        sys.exit(1)
    
    print(f"Demarrage du workflow pour {len(product_names)} produit(s)...")
    
    scraper = ProductScraper()
    prompt_gen = PromptGenerator()
    
    spreadsheet_id = os.environ.get('GOOGLE_SHEET_ID')
    credentials_path = os.environ.get('GOOGLE_CREDENTIALS_PATH', 'google_credentials.json')
    
    if not spreadsheet_id:
        print("Erreur: GOOGLE_SHEET_ID non defini.")
        sys.exit(1)
    
    sheets = SheetsManager(spreadsheet_id, credentials_path)
    
    sheet_name = datetime.now().strftime('%Y-%m-%d')
    worksheet = sheets.create_or_get_sheet(sheet_name)
    
    results = []
    not_found = []
    
    for product_name in product_names:
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
            
            results.append({
                'name': product_info['name'],
                'status': 'Succes',
                'image': product_info['image_url']
            })
        else:
            print(f"Produit non trouve: {product_name}")
            not_found.append(product_name)
            results.append({
                'name': product_name,
                'status': 'Non trouve',
                'image': ''
            })
    
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if webhook_url:
        sheet_url = sheets.get_sheet_url(worksheet)
        
        message = "Workflow termine !\n\n"
        message += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        message += "Resultats:\n"
        
        for r in results:
            emoji = "✅" if r['status'] == 'Succes' else "❌"
            message += f"{emoji} {r['name']}: {r['status']}\n"
        
        if not_found:
            message += f"\nProduits non trouves ({len(not_found)}):\n"
            for p in not_found:
                message += f"- {p}\n"
        
        message += f"\nGoogle Sheet: {sheet_url}"
        
        send_discord_notification(webhook_url, message)
        print("Notification Discord envoyee.")
    
    print(f"Workflow termine avec succes !")
    print(f"Sheet: {sheets.get_sheet_url(worksheet)}")

if __name__ == '__main__':
    main()
