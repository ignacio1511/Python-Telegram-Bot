import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("RetoSeiken2022_Mensajes_Telegram").sheet1

#### - BIBLIOTECA DE MENSAJES - ####

motivation = sheet.col_values(1) 

nutrition = sheet.col_values(2)
