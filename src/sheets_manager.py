import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

class SheetsManager:
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, spreadsheet_id, credentials_path='google_credentials.json'):
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = credentials_path
        self.client = None
        self.spreadsheet = None
        self._connect()
    
    def _connect(self):
        credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=self.SCOPES
        )
        self.client = gspread.authorize(credentials)
        self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
    
    def create_or_get_sheet(self, sheet_name=None):
        if sheet_name is None:
            sheet_name = datetime.now().strftime('%Y-%m-%d')
        
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            print(f"Feuille '{sheet_name}' trouvee.")
            return worksheet
        except gspread.WorksheetNotFound:
            worksheet = self.spreadsheet.add_worksheet(
                title=sheet_name,
                rows=1000,
                cols=10
            )
            print(f"Nouvelle feuille '{sheet_name}' creee.")
            
            headers = ['Nom du produit', 'Image', 'Lien image', 'Prompt']
            worksheet.append_row(headers)
            
            return worksheet
    
    def add_product(self, worksheet, product_name, image_url, prompt):
        image_formula = f'=IMAGE("{image_url}")' if image_url else ''
        row = [product_name, image_formula, image_url, prompt]
        worksheet.append_row(row)
        print(f"Produit ajoute : {product_name}")
    
    def get_sheet_url(self, worksheet):
        sheet_id = worksheet.id
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit#gid={sheet_id}"
