import json
import os
import sys
import urllib.request

API_URL = 'https://api.nature.global/1/appliances'
REMOTE_NAME = 'RM-YSR04'


def get_appliances(token):
    req = urllib.request.Request(API_URL, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def find_appliance_id(appliances, remote_name):
    for appliance in appliances:
        model = appliance.get('model') or {}
        if model.get('remote_name', '').upper() == remote_name.upper():
            return appliance['id']
    return None


def main():
    token = os.environ.get('NATURE_REMO_TOKEN')
    if not token:
        sys.exit('環境変数 NATURE_REMO_TOKEN にアクセストークンを設定してください')

    appliances = get_appliances(token)
    appliance_id = find_appliance_id(appliances, REMOTE_NAME)

    if appliance_id is None:
        sys.exit(f'{REMOTE_NAME} のリモコンが見つかりませんでした')

    print(appliance_id)


if __name__ == '__main__':
    main()
