import os
import requests

#channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_secret = 'b5ef5faad577943ab91961106aa23cfb'
#channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_access_token = '6gJmycFl4wqU5BARAEQt+Q4gMorbAyZ7+4+5poIcPCqIbrhM6HIXNBDMYdG9YkfOeI+arsGCYbHhqnACyj06LZSmszL2lE01ahtFEiFwfq8kyji5V6LWNQQ+PvspLDvW8xgFWwwHCsB2uKyb2YrY2gdB04t89/1O/w1cDnyilFU='

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random 

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(channel_access_token)
# Channel Secret
handler = WebhookHandler(channel_secret)
user_id = 'user_id'

# @app.route("/push_function/<string:push_text_str>")
# def push_message(push_text_str):
#     line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))
#

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#keywords = ["哪有之前準現在就不準的","我們需要大學以上程度，不是國中生","你們這樣效率很差","乾我屁事"]

# 處理訊息
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#     if "老M掰" in event.message.text:
#        bye_message = "好啊" #離開群組訊息
#        line_bot_api.reply_message(event.reply_token, TextMessage(text=bye_message))
#        line_bot_api.leave_group(event.source.group_id)
#     elif "M" in event.message.text:
#        message = TextSendMessage(text=random.choice(keywords))
#        line_bot_api.reply_message(event.reply_token, message)

@app.route('/')
def index():
    return 'Wayne\'s LINE Bot'

# 當機器人加入到一個群組，第一次顯示的訊息
@handler.add(JoinEvent)
def handle_join(event):
    welcome_message = ""  #進入群組訊息
    line_bot_api.reply_message(event.reply_token, TextMessage(text=welcome_message))
    print("加入的事件: %s" % event)
    print("加入事件的資訊: %s" % event.source)


@handler.add(LeaveEvent)
def handle_leave(event):
    print("離開的事件: %s" % event)
    print("離開事件的資訊: %s" % event.source)
    
    
def GetPrice(symbol):
    try:
        price = requests.get('https://api.binance.com/api/v3/ticker/price', params={'symbol': symbol}).json()['price']
    except Exception as e:
        print ('Error! problem is {}'.format(e.args[0]))
    return float(price)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    while True:
        price = GetPrice("BTCUSDT")
        print ("price=%f" %price)
        message = TextSendMessage(text=price)
        line_bot_api.reply_message(event.reply_token, message)
        time.sleep(10)
