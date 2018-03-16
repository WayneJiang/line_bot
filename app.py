from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage, SourceUser
)

import os

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print('Request body: ' + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        # if not isinstance(event.message, TextMessage):
        #     continue

        # if isinstance(event.message, StickerMessage):
            
        # elif isinstance(event.message, TextMessage):
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=event.message.text)
        #     )
        
        line_bot_api.push_message('Uf3f2e1fd512672a9bfaf7b5fb28ed687',TextSendMessage(text='Send'))
        # if isinstance(event.source,SourceUser):
        #     profile = line_bot_api.get_profile(event.source.user_id)
        #     print(profile.display_name)
        #     print(profile.user_id)
        #     print(profile.picture_url)
        #     print(profile.status_message)
            # line_bot_api.reply_message(
            #     event.reply_token,
            #     TextSendMessage(text='name='+profile.display_name+'\n'
            #     +'user id='+profile.user_id+'\n'
            #     +'picture url='+profile.picture_url+'\n'
            #     +'status message='+profile.status_message)
            # )
    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
