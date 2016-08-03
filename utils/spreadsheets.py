spreadsheetId = '1mjusB5yRpbSO3tbMaVkqqCGzHOkH1Wb0Y7N9ABu5bJ4'

def get_values(range, service, decorator, defaultValue=[]):
    return service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=range
    ).execute(
        http=decorator.http()
    ).get('values', defaultValue)


def update_values(range, body, service, decorator):
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range=range,
        valueInputOption='RAW',
        body=body
    ).execute(
        http=decorator.http()
    )
