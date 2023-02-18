SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'FULL PATH TO JSON KEY FROM GOOGLE API CONSOLE'
VIEW_ID = 'YOU GOOGLE ANALYTICS VIEW ID'

def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics


analytics = initialize_analyticsreporting()

