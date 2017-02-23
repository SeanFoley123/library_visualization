import requests as r
import json
import pprint
import os

from config import USER_ID, PASSWORD, PROFILE

pp = pprint.PrettyPrinter(indent=1)

DIR_PATH = os.path.dirname(__file__)
TOKEN_FILE = os.path.join(DIR_PATH, "auth.json")

HEADERS = {'content-type': 'application/json', 'accept': 'application/json'}
BASE_URL = "https://eds-api.ebscohost.com"
AUTH_URL = BASE_URL + "/authservice/rest/UIDAuth"
SESSION_URL = BASE_URL + "/edsapi/rest/CreateSession"

AUTH_PAYLOAD = {"UserId": USER_ID, "Password": PASSWORD, "InterfaceId": "edsapi_console"}
SESSION_PAYLOAD = {"Profile": PROFILE, "Guest": "n", "Org": None}


def set_token(name, url, payload, headers):
    res = r.post(url, json.dumps(payload), headers=headers)
    credentials = get_tokens()
    with open(TOKEN_FILE, 'r+') as auth:
        credentials["AuthToken"] = credentials.get("AuthToken", "")
        credentials["SessionToken"] = credentials.get("SessionToken", "")
        credentials[name] = res.json()[name]
        auth.seek(0)
        auth.truncate()
        auth.write(json.dumps(credentials))


def set_tokens():
    set_token('AuthToken', AUTH_URL, AUTH_PAYLOAD, HEADERS)
    set_token('SessionToken', SESSION_URL, SESSION_PAYLOAD, HEADERS)


def get_tokens(open_auth_file=None):
    try:
        with open(TOKEN_FILE, 'r') as auth:
            credentials = json.loads(auth.read())
    except (IOError, ValueError) as e:
        credentials = {"AuthToken": "", "SessionToken": ""}
        with open(TOKEN_FILE, 'w') as auth:
            auth.write(json.dumps(credentials))
    return credentials


def search(query_term):
    tokens = get_tokens()
    HEADERS['x-authenticationToken'] = tokens['AuthToken']
    HEADERS['x-sessionToken'] = tokens['SessionToken']
    cat_url = BASE_URL + "/edsapi/publication/Search?query=%s&resultsperpage=100&highlight=n" % query_term
    res = r.get(cat_url, headers=HEADERS)
    if res.json().get('ErrorNumber'):
        set_tokens()
        return search(query_term)
    return res.json()

if __name__ == "__main__":
    cats_search = search("cats")
    pp.pprint(cats_search)
