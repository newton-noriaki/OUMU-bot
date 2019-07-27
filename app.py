from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
####TODO#########

import os
from os.path import join, dirname
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv(join(dirname(__file__),'.env'))

line_bot_api = LineBotApi(os.environ.get('linebot_token'))
handler = WebhookHandler(os.environ.get('linebot_secret'))

####TODO##########
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # -*- coding: utf-8 -*-
    import pya3rt

    apikey = "DZZEqN4NXwlVu2ONNpRb0N7aMAu8lx2S"
    client = pya3rt.TalkClient(apikey)


    word = event.message.text
    res = client.talk(word)
    #print(res['results'][0]['reply'])

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=res['results'][0]['reply']))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    app.run()