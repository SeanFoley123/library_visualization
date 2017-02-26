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

    if not res.json().get(name):
        return credentials

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
    query_term = query_term.replace(' ', '+')
    tokens = get_tokens()
    HEADERS['x-authenticationToken'] = tokens['AuthToken']
    HEADERS['x-sessionToken'] = tokens['SessionToken']
    cat_url = BASE_URL + "/edsapi/publication/Search?query=%s&searchmode=smart&resultsperpage=100&highlight=n" % query_term
    res = r.get(cat_url, headers=HEADERS)
    if res.json().get('ErrorNumber'):
        set_tokens()
        return search(query_term)
    return res.json()


def create_forest(data):                # Nests dicts for subject hierachies 
    subjects = [facet for facet in data['SearchResult']['AvailableFacets'] if facet['Id'] == 'SubjectPubDb'][0]['AvailableFacetValues']

    def add_subject(pos, subject, node, ct):        # Pos = position in list subject, node = a dict, ct = count in that subject
        key = subject[pos]                          # The word we're currently looking at
        if pos == len(subject) - 1:                   # If you're at the lowest level, make it a count
            node[key] = ct
        else:                                       # Otherwise, make a new child node or update an existing one
            add_subject(pos + 1, subject, node.setdefault(key, {}), ct)
    forest = {}
    for subject_dict in subjects:                   # Add each subject path to the forest
        add_subject(0, subject_dict['Value'].split(" / "), forest, subject_dict['Count'])
    return forest

if __name__ == "__main__":
    cats_search = search("cats")
    pp.pprint(create_forest(cats_search))
    # pp.pprint(cats_search)
