import requests
import sys
from get_docker_secret import get_docker_secret
import json
import os

# consumer_id = ""
# consumer-secret = ""

refresh_token = ""


def get_secret_mount_path():
    secrets_mount_path = os.getenv("secrets_mount_path")
    if secrets_mount_path is None or secrets_mount_path == "":
        secrets_mount_path = "/var/run/secrets/"
    return secrets_mount_path


def set_global():
    # global consumer_id
    # global consumer-secret
    global refresh_token

#    consumer_id = os.getenv("consumer_id")
#    if consumer_id == None:
#        print("consumer_id is not set")
#        sys.exit(1)
    secrets_mount_path = get_secret_mount_path()
    refresh_token = get_docker_secret("refresh_token", safe=True,
                                      secrets_dir=secrets_mount_path)
    if refresh_token is None:
        print("refresh_token is not set")
        sys.exit(1)
#    consumer-secret = get_docker_secret("consumer-secret", safe=True,
#                                        secrets_dir="/var/openfaas/secrets/")
#    if consumer-secret == None:
#        print("consumer-secret is not set")
#        sys.exit(1)


def handle_upcoming_events():
    payload = {'group_urlname': 'SHITY-Hiking-and-Outdoors',
               'access_token': 'refresh_token'}
    resp = requests.get('https://api.meetup.com/2/events', params=payload)
    resp.raise_for_status()
    data = resp.json()
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

    if handler is not None:
        set_global()
        return handler()

    return ""
