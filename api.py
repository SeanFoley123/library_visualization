import requests as r
import json as j
import pprint

from config import USER_ID, PASSWORD, PROFILE

pp = pprint.PrettyPrinter(indent=1)

base_url = "https://eds-api.ebscohost.com"
headers = {'content-type': 'application/json', 'accept': 'application/json'}

auth_url = base_url + "/authservice/rest/UIDAuth"
auth_payload = {"UserId": USER_ID, "Password": PASSWORD, "InterfaceId": "edsapi_console"}
a = r.post(auth_url, j.dumps(auth_payload), headers=headers)

headers['x-authenticationToken'] = a.json()['AuthToken']

session_payload = {"Profile": PROFILE, "Guest": "n", "Org": None}
session_url = base_url + "/edsapi/rest/CreateSession"
a = r.post(session_url, j.dumps(session_payload), headers=headers)

headers['x-sessionToken'] = a.json()['SessionToken']

cat_url = base_url + "/edsapi/publication/Search?query=cats&resultsperpage=20&pagenumber=1&sort=relevance&highlight=y&includefacets=y&view=brief&autosuggest=n"
a = r.get(cat_url, headers=headers)
pp.pprint(a.json())
