import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("RetoSeiken2022_Mensajes_Telegram").sheet1

#### - BIBLIOTECA DE MENSAJES - ####

mensajes__motivacion_mañana = sheet.col_values(1) 

tips_alimentacion = sheet.col_values(2) 

trigger_mañana = sheet.col_values(3)

trigger_tarde = sheet.col_values(4)

trigger_noche = sheet.col_values(5)