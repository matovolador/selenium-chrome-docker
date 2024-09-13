import gspread
from settings import Settings
from google.oauth2.service_account import Credentials


class GoogleSheetReader():
    def __init__(self, sheet):
        # Path to the service account key file
        key_file = Settings.GSHEET_KEY_JSON_PATH

        # Define the scope
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

        # Authenticate with Google
        credentials = Credentials.from_service_account_file(
            key_file, scopes=scopes)

        # Connect to Google Sheets
        self.client = gspread.authorize(credentials)

        # Open the Google Sheet by name or URL
        self.spreadsheet = self.client.open(sheet)

    def read(self, sheet_index=0):
        output = []
        # Select the worksheet
        worksheet = self.spreadsheet.get_worksheet(sheet_index)

        # Get all the data
        data = worksheet.get_all_values()

        # Extract column names (first row) and columns (remaining rows)
        column_names = data[0]  # First row
        columns = list(zip(*data[1:]))  # Transpose rows to columns

        # Print column names and their respective columns
        for col_name, col_data in zip(column_names, columns):
            # Replace empty strings with a default value like None or 'N/A'
            processed_col_data = [val if val !=
                                  '' else None for val in col_data]
            output.append({"column": col_name, "data": processed_col_data})
        return output
