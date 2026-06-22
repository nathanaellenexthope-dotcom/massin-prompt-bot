#!/usr/bin/env python3
import gspread
from google.oauth2.service_account import Credentials


class SheetsManager:
    def __init__(self, spreadsheet_id: str, credentials_path: str):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self.client = self._authorize()
    
    def _authorize(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
        return gspread.authorize(creds)
    
    def create_or_get_sheet(self, sheet_name: str):
        spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        try:
            worksheet = spreadsheet.worksheet(sheet_name)
            print(f"Sheet existant trouve: {sheet_name}")
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="4")
            worksheet.append_row(["Nom du produit", "Image URL", "Lien Image", "Prompt"])
            print(f"Nouveau sheet cree: {sheet_name}")
        return worksheet
    
    def add_product(self, worksheet, product_name: str, image_url: str, prompt: str):
        worksheet.append_row([product_name, image_url, image_url, prompt])
        print(f"Produit ajoute: {product_name}")
    
    def get_sheet_url(self, worksheet):
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit#gid={worksheet.id}"
