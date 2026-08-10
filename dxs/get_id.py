import os
import sys
import requests
import json

Token = os.environ.get('NATURE_REMO_TOKEN')
if not Token:
    sys.exit('環境変数 NATURE_REMO_TOKEN にアクセストークンを設定してください')

headers = {
    "Authorization": f"Bearer {Token}"
}
r = requests.get(
    "https://api.nature.global/1/appliances",
    headers=headers
)

print(json.dumps(r.json(), indent=2, ensure_ascii=False))
