import requests
import pandas as pd
from io import StringIO
from logger import Logger

logging = Logger().get_logger()


class PublicGoogleSheetReader:
    def __init__(self, sheet_id):
        """
        Args:
            sheet_id (str): The Google Sheet ID from the sheet URL.
        """
        self.sheet_id = sheet_id
        self.csv_url = f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv"

    def read(self):
        """
        Fetches the Google Sheet data and loads it into a pandas DataFrame and a python list of dicts.
        """
        response = requests.get(self.csv_url, timeout=30)
        response.raise_for_status()  # Raises HTTPError if the request was unsuccessful
        df = pd.read_csv(StringIO(response.text))
        # Prepare output list of dicts
        output = []
        for column_name in df.columns:
            column_data = df[column_name].fillna('').tolist()
            output.append({"column": column_name, "data": column_data})

        return {'data_frame': df, 'dict': output}
