import os
import sys
import requests

TOKEN = os.environ.get('NATURE_REMO_TOKEN')
if not TOKEN:
    sys.exit('環境変数 NATURE_REMO_TOKEN にアクセストークンを設定してください')

SIGNAL_ID = "9a5cdc99-8cfc-4844-ac7c-235a58ef3db4"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

r = requests.post(
    f"https://api.nature.global/1/signals/{SIGNAL_ID}/send",
    headers=headers
)

print(r.status_code)
print(r.text)


