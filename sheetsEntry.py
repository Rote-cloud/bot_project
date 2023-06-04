import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from actionDB import ActionDB
from setting import CRED

class SheetsEntry:
    def __init__(self):
        self.credentials = None
        self.client = None
        self.service = None

        self.auth_google_sheets()

    def auth_google_sheets(self):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive"]
        flow = InstalledAppFlow.from_client_secrets_file(
            CRED, scope)
        self.credentials = flow.run_local_server(port=0)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.client = gspread.authorize(self.credentials)

    def data_entry(self, df, user_name):
        spreadsheet_details = {
            'properties': {
                'title': 'weather_' + user_name
            }
        }
        sheet = self.service.spreadsheets().create(body=spreadsheet_details,
                                                   fields='spreadsheetId').execute()
        sheetId = sheet.get('spreadsheetId')
        sheet = self.client.open("weather_" + user_name).sheet1
        sheet.update([df.columns.values.tolist()] + df.values.tolist())

        spreadsheet = self.service.spreadsheets().get(spreadsheetId=sheetId).execute()
        url = spreadsheet['spreadsheetUrl']
        db = ActionDB().add(user_name, url)

        return url
