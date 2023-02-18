import gspread


class GSWriter:

    def __init__(self, credentials_file, gs_url):
        self.credentials_file = credentials_file
        self.gs_url = gs_url

    def write(self):
        gc = gspread.service_account(filename=self.credentials_file)
        sh = gc.open_by_url(self.gs_url)
        worksheet = sh.get_worksheet(0)
        worksheet.update('B3', 'sex')