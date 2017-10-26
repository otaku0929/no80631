import requests
import re
import random
import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'



def ask():
    url = "http://wisdomer2002.pixnet.net/blog/post/224560-%E5%AA%BD%E7%A5%96%E7%B1%A4%E8%A9%A960%E9%A6%96"
    request = requests.get(url)
    ytcontent = request.content
    soup = BeautifulSoup(ytcontent, "html.parser")

    content = ""

    alist = soup.select("div.article-content li a" )
    random.shuffle(alist)
    askdata = alist[0]

                                    
    url=askdata.get("href")
    text=askdata.get_text()

    content = '{}\n詳解:{}\n\n'.format(text,url)
    
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    

    if event.message.text == "抽":
        client = ImgurClient('e42cc11418f9001', 'cd8239b7a2bd0f55161e8b1124cdc6bdb3fd8b06')
        images = client.get_album_images('Ya0RbuE')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
     if event.message.text == "抽籤":
        content = ask()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
 if __name__ == '__main__':
    app.run()

