
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
import requests # pip install requests
import urllib3
app = Flask(__name__)
line_bot_api =
LineBotApi('eypGeGLl5S/n8VBnH/XN0MdXDAgRgsjmr0O7hVa+DWlfUMDxGRHc1sUbe8u99zTMJtOJIzuVNYIFOVAcg6F1v1d4Bt2fn8Zd5pZdTYa572tqUBB1+yKh6H4mxka6XzNUyqrBBYNfFt963IZEhQ+LUgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6300e45cda84767687909c6059b2850c')
APPID="LEDControl1"
KEY = "K5RtqjUJndtV2em"
SECRET = "12c7fCo9RLw0bdu2rNAvtHXrM"
Topic = "/LED_Control"
url = 'https://api.netpie.io/topic/' + str(APPID) + str(Topic)
#curl -X PUT "https://api.netpie.io/topic/LineBotRpi/LED_Control" -d "ON" -u Jk0ej35pLC7TVr1:edWzwTUkzizhlyRamWWq6nF9I
urlRESTAPI = 'https://api.netpie.io/topic/' + str(APPID) + str(Topic) + '?auth=' + str(KEY) + ':' + str(SECRET)
#https://api.netpie.io/topic/LineBotRpi/LED_Control?auth=Jk0ej35pLC7TVr1:edWzwTUkzizhlyRamWWq6nF9I
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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
if "on" in str(event.message.text):
line_bot_api.reply_message(event.reply_token,TextSendMessage(text='ON LED'))
#REST API NETPIE ON LED
r = requests.put(url, data = {'':'ON'} , auth=(str(KEY),str(SECRET)))
elif "off" in str(event.message.text):
line_bot_api.reply_message(event.reply_token,TextSendMessage(text='OFF LED'))
#REST API NETPIE OFF LED
r = requests.put(url, data = {'':'OFF'} , auth=(str(KEY),str(SECRET)))
elif "temp?" in str(event.message.text):
#REST API NETPIE read sensor value
r = requests.put(url, data = {'':'temp?'} , auth=(str(KEY),str(SECRET)))
http = urllib3.PoolManager()
response = http.request('GET',urlRESTAPI) # read data from publish retain
line_bot_api.reply_message(event.reply_token,TextSendMessage(text=((str(response.data)).split('"')[7]) + " °C"))
else:
line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
if __name__ == "__main__":
app.run()
