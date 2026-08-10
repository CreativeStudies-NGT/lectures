from slack_sdk import WebClient

TOKEN   = 'xoxb-xxxx-...'
CHANNEL = 'C0XXXXXXXXX'

client = WebClient(token=TOKEN)

# テキストのみ投稿
client.chat_postMessage(
    channel=CHANNEL,
    text='hello',
    username='通知Bot',
    icon_emoji=':robot_face:',
)

# 写真付き投稿
client.files_upload_v2(
    channel=CHANNEL,
    file='photo.jpg',
    title='写真',
    initial_comment='写真を投稿します',
)
