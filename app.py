from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
)

from linebot.models import (
    SourceUser
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
            print(''+event.SourceUser.user_id)
        #     continue
        # if not isinstance(event.message, TextMessage):
        #     continue

        # if isinstance(event.message, StickerMessage):
            
        # elif isinstance(event.message, TextMessage):
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=event.message.text)
        #     )


    return 'OK'

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
