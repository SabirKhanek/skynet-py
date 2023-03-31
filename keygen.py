import os
import requests


def validate_key(key):
    url = f"https://api.keygen.sh/v1/accounts/{os.environ['keygen_acc']}/licenses/actions/validate-key"
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json'
    }
    data = {'meta': {'key': key}}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_json = response.json()
        if 'meta' in response_json and 'code' in response_json['meta']:
            return response_json['meta']['code'] == 'VALID'
    return False


def get_key(meta={"name": "unspecified"}):
    license_attrs = {
        "name": meta["name"] if "name" in meta else "unspecified",
    }
    url = f"https://api.keygen.sh/v1/accounts/{os.environ['keygen_acc']}/licenses"
    headers = {
        'Authorization': f"Bearer {os.environ['keygen_api_key']}", 'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json'
    }
    data = {
        'data': {
            'type': 'license',
            'relationships': {
                "policy": {
                    "data": {
                        "type": "policy",
                        "id": os.environ['keygen_policy_id']
                    }
                }
            },
            "attributes": license_attrs
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        response_json = response.json()
        if 'data' in response_json and 'attributes' in response_json['data'] and 'key' in response_json['data']['attributes']:
            return response_json['data']['attributes']['key']
    return None


# print(get_key())

# key = "467D55-4EF2A2-7BBE84-A45626-B3A5A0-V3"
# is_valid = validate_key(key)
# print(is_valid)  # True if key is valid, False otherwise
