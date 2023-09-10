from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    ImageSendMessage,
    LocationSendMessage,
    StickerSendMessage,
)

from crawler.main import get_big_lottory

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


def index(request):
    return HttpResponse("chatbot v1.3")


@csrf_exempt  # 安全請求(必寫)
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                # 此兩物件為相同為true(即為可辨識)就運行，events表user傳入之訊息
                text = event.message.text
                print(text)
                if text == "1":
                    # message = "早安"
                    message = TextSendMessage(text="早安")
                elif text == "2":
                    message = TextSendMessage(text="午安")
                elif "樂透" in text:
                    nums = get_big_lottory()
                    message = TextSendMessage(text=nums)
                elif "捷運" in text:
                    if "台中" in text:
                        img_url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taichung/20201112_zh.png?v=2"
                    elif "高雄" in text:
                        img_url = "https://www.krtc.com.tw/Content/userfiles/images/guide-map.jpg?v=c24_1"
                    else:
                        img_url = "https://web.metro.taipei/pages/assets/images/routemap2023n.png"
                    message = ImageSendMessage(
                        original_content_url=img_url, preview_image_url=img_url
                    )
                elif "台北車站" in text:
                    message = LocationSendMessage(
                        title="台北車站",
                        address="地址",
                        latitude=25.047778,
                        longitude=121.517222,
                    )
                elif "桃園" in text:
                    message = StickerSendMessage(package_id=446, sticker_id=1988)

                else:
                    message = TextSendMessage(text="不知道")
                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        message,
                    )
                except Exception as e:
                    print(e)
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
