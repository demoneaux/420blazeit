# [420blazeit](https://vjcblazer.appspot.com/) [![Build Status](https://travis-ci.org/vjmakers/420blazeit.svg?branch=master)](https://travis-ci.org/vjmakers/420blazeit)

An online platform for loaning VJC blazers integrated with Google Spreadsheets.

## Getting Started

1. Install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python).
2. Install the [Google API Client Library for Python](https://developers.google.com/api-client-library/python/):<br>
   `pip install -r requirements.txt -t lib`.
3. Create a OAuth Client ID for Google Spreadsheets using [Google Cloud Console](https://console.cloud.google.com/apis/credentials?project=vjcblazer).<br>
   Use `http://localhost:8080/oauth2callback` (depending on which port you run the app on) as the redirect URL.<br>
   Alternatively, if there are already OAuth Client IDs in the Console, you can use them too.
4. Download and save the JSON file as `client_secrets.json`.
5. Run the app using the App Engine Launcher.

**Notes**:

* The email `loans.vjc@gmail.com` must be used.
* Some of the pages require admin access.
