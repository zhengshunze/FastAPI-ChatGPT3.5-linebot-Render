# -*- coding: utf-8 -*-

import logging, uvicorn
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage





################################################################
import openai, os
	
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("BASE_URL")
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET")) 



app = FastAPI()
# Line Bot config

@app.get("/") # 指定 api 路徑 (get方法)
async def hello():
	return "Hello World from Flask in a uWSGI Nginx Docker container with \
	     Python 3.8 (from the example template)"

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handling_message(event):
    #replyToken = event.reply_token
    
    if isinstance(event.message, TextMessage):

        user_message = event.message.text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=user_message))


