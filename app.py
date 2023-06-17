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

app = Flask(__name__)

line_bot_api = LineBotApi('Fqt4AFFQqL1wjAs1fXU+AKJsQyKcYaCsaVre3mf2q8OSrXwzl1BckN8JS751lfgnuL/hCH/y7YrLUg9j9+jbXnddhiKP2xOYOA6CkcvyvQxMKgGNgfMqXv/sKi0M3vZgmsj/lpsqX8k8Rohi8Jh0iwdB04t89/1O/w1cDnyilFU=)
handler = WebhookHandler('20288aa68d4860d8fd0a1b225b8b0402')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()