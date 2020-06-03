from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookParser, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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


handler = WebhookHandler(channel_secret)


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
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   if event.message.text=="老高":
              line_bot_api.reply_message(
                 event.reply_token,
                 TextSendMessage(text='又在幻想')
              )

@handler.add(JoinEvent)
def handle_join(event):
    welcome_message = "怎樣？可憐那"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=welcome_message))
    print("加入的事件: %s" % JoinEvent)

@handler.add(LeaveEvent)
def handle_leave(event):
    message = "可憐那"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=message))
    print("離開 事件: %s" % event)
    print("離開事件的資訊: %s" % event.source)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port)
