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
from crawler.train import get_stations, get_train_data2
from datetime import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)

menu = ""
menu_str = ""
train_str = ""
stations = {}
step = 0
startStation, endStation, rideDate, startTime, endTime = "", "", "", "", ""


def index(request):
    return HttpResponse("chatbot v1.2")


def get_menu():
    global menu, menu_str, stations
    if menu_str == "":
        stations = get_stations()
        menu = {i + 1: station for i, station in enumerate(stations)}
        count = 0
        for k, v in menu.items():
            menu_str += "{:2}.{:4}".format(k, v)
            count += 1
            if count % 4 == 0:
                menu_str += "\n"
    # return menu_str  #因有global menu_str就不用寫


@csrf_exempt  # 安全請求(必寫)
def callback(request):
    global menu, menu_str, stations, step, startStation, endStation, rideDate, startTime, endTime
    get_menu()
    print(menu_str)

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
                text = event.message.text
                print(text)
                try:
                    if text == "exit":
                        text = "感謝您的使用~ (0可重新查詢)"
                        step = 0
                    elif text == "0" and step == 0:
                        text = menu_str + "\n請輸入起始站點:"
                        step += 1
                    elif step == 1:
                        # {1:臺北}
                        startStation = menu[eval(text)]
                        text = f"起始站:({startStation})，請輸入終止站:"
                        step += 1
                    elif step == 2:
                        endStation = menu[eval(text)]
                        text = f"({startStation})-({endStation})，請輸入乘車日期(輸入.為今日):"
                        step += 1
                    elif step == 3:
                        if text == ".":
                            rideDate = datetime.now().strftime("%Y/%m/%d")
                        else:
                            rideDate = text
                        text = f"({startStation})-({endStation})，乘車日期:({rideDate})\n請輸入查詢起始時間(輸入.為現在時間):"
                        step += 1
                    elif step == 4:
                        if text == ".":
                            startTime = datetime.now().strftime("%H:%M")
                        else:
                            startTime = text
                        text = f"({startStation})-({endStation})，乘車日期:({rideDate}) 時間:({startTime})\n請輸入查詢終止時間(輸入.為23:59):"
                        step += 1
                    elif step == 5:
                        if text == ".":
                            endTime = "23:59"
                        else:
                            endTime = text
                        text = get_train_data2(
                            stations[startStation],
                            stations[endStation],
                            rideDate,
                            startTime,
                            endTime,
                        )
                        text += "\n感謝您的使用~ (0可重新查詢)"
                        step = 0
                except Exception as e:
                    print(e)
                    text = "輸入不正確! 請重新輸入...(0可重新查詢)"
                message = TextSendMessage(text=text)
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
