import requests
import sys
from get_docker_secret import get_docker_secret
import json

#consumer_id = ""
#consumer-secret = ""
refresh_token = ""


def set_global():
#    global consumer_id
#    global consumer-secret
    global refresh_token

#    consumer_id = os.getenv("consumer_id")
#    if consumer_id == None:
#        print("consumer_id is not set")
#        sys.exit(1) 
    refresh_token = get_docker_secret("refresh_token", safe=True, secrets_dir="/var/openfaas/secrets/", envvar=True) 
    if refresh_token == None:
        print("refresh_token is not set")
        sys.exit(1) 
#    consumer-secret = get_docker_secret("consumer-secret", safe=True, secrets_dir="/var/openfaas/secrets/")
#    if consumer-secret == None:
#        print("consumer-secret is not set")
#        sys.exit(1) 


def handle_upcoming_events():
    payload = {'group_urlname': 'SHITY-Hiking-and-Outdoors', 'access_token': 'refresh_token'}
    r = requests.get('https://api.meetup.com/2/events', params=payload)
    r.raise_for_status()
    data = r.json()
    
    result = {}
    result['events'] = data['results']
    result['count'] = data['meta']['count']

    return json.dumps(result) 


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    handler = None
    if req == "upcoming-events":
         handler = handle_upcoming_events

    if handler != None:
        set_global()
        return handler()

    return ""
