from __future__ import print_function
import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import psycopg2
from os import environ

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/opt/app-root/secrets/google-services-credentials.json'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = environ["SPREADSHEET_ID"]
RANGE_NAME = 'Data'

COUNT_PARTICIPANTS_QUERY= """
    SELECT count (*)
    FROM
        studyparticipant
    """

COUNT_QUEUE_QUERY= """
    SELECT count (*)
    FROM
        queue
    """

COUNT_QUEUE_DISTINCT_QUERY= """
    SELECT count (distinct subject_id)
    FROM
        queue
    """

def main():
    ## STEP 1: Get data from DB ##
    conn = psycopg2.connect(host=environ["DB_HOST"], port=environ["DB_PORT"], dbname=environ["database-name"], user=environ["database-user"], password=environ["database-password"])
    cursor = conn.cursor()
    
    cursor.execute(COUNT_PARTICIPANTS_QUERY)
    participant_count = int(cursor.fetchone()[0])
    
    cursor.execute(COUNT_QUEUE_QUERY)
    queue_count = int(cursor.fetchone()[0])

    cursor.execute(COUNT_QUEUE_DISTINCT_QUERY)
    queue_count_distinct = int(cursor.fetchone()[0])

    now = datetime.datetime.now()
    date = now.strftime("%d") + "." +  now.strftime("%m") + "." + now.strftime("%G")
    
    values = [[date, participant_count, queue_count, queue_count_distinct]]
    body = {'values': values}

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    try:
        service = build('sheets', 'v4', credentials=credentials)
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, body=body, valueInputOption="RAW").execute()
        print(f'${result.get("updates").get("updatedCells")} cells appended')

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()