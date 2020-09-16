#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''

整體功能描述

'''


# In[2]:


'''

Application 主架構

'''

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json, re, sys

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))
server_url=secretFileContentJson.get("server_url")

#複製的，載入基礎設定檔
channel_access_token = secretFileContentJson.get("channel_access_token")
self_user_id = secretFileContentJson.get("self_user_id")
rich_menu_id = secretFileContentJson.get("rich_menu_id")


# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/素材" , static_folder = "./素材/")

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
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



# In[3]:


'''

消息判斷器

讀取指定的json檔案後，把json解析成不同格式的SendMessage

讀取檔案，
把內容轉換成json
將json轉換成消息
放回array中，並把array傳出。

'''

# 引用會用到的套件
from linebot.models import (
    ImagemapSendMessage,TextSendMessage,ImageSendMessage,LocationSendMessage,FlexSendMessage,VideoSendMessage
)

from linebot.models.template import (
    ButtonsTemplate,CarouselTemplate,ConfirmTemplate,ImageCarouselTemplate
    
)

from linebot.models.template import *

def detect_json_array_to_new_message_array(fileName):
    
    #開啟檔案，轉成json   #記得加encoding = 'utf-8'
    with open(fileName, encoding = 'utf-8') as f:
        jsonArray = json.load(f)
    
    # 解析json
    returnArray = []
    for jsonObject in jsonArray:

        # 讀取其用來判斷的元件
        message_type = jsonObject.get('type')
        
        # 轉換
        if message_type == 'text':
            returnArray.append(TextSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'imagemap':
            returnArray.append(ImagemapSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'template':
            returnArray.append(TemplateSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'image':
            returnArray.append(ImageSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'sticker':
            returnArray.append(StickerSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'audio':
            returnArray.append(AudioSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'location':
            returnArray.append(LocationSendMessage.new_from_json_dict(jsonObject))
        elif message_type == 'flex':
            returnArray.append(FlexSendMessage.new_from_json_dict(jsonObject))  
        elif message_type == 'video':
            returnArray.append(VideoSendMessage.new_from_json_dict(jsonObject))    


    # 回傳
    return returnArray


# In[4]:


'''

handler處理關注消息

用戶關注時，讀取 素材 -> 關注 -> reply.json

將其轉換成可寄發的消息，傳回給Line

'''

# 引用套件
from linebot.models import (
    FollowEvent
)

"""
引用套件
連接資料庫

"""
#後續若要把紀錄log檔儲存，再另外加入



'''

# 新好友歡迎(insert user id)
新使用者加入，即把使用者user_id匯入至kafka

'''

#匯入套件
import time, requests

# 關注事件處理
@handler.add(FollowEvent)
def process_follow_event(event):
    
    # 讀取並轉換
    result_message_array =[]
    replyJsonPath = "素材/關注/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
        
    #複製的 將菜單綁至用戶上
    user_id = line_bot_api.get_profile(event.source.user_id)
    linkRichMenuId = rich_menu_id
    linkMenuEndpoint = 'https://api.line.me/v2/bot/user/%s/richmenu/%s' % (event.source.user_id, linkRichMenuId)
    linkMenuRequestHeader = {'Content-Type': 'image/jpeg', 'Authorization': 'Bearer %s' % channel_access_token}
    lineLinkMenuResponse = requests.post(linkMenuEndpoint, headers=linkMenuRequestHeader)
    app.logger.info("Link Menu to %s status :" % user_id, lineLinkMenuResponse)

    # 消息發送
    line_bot_api.reply_message(
        event.reply_token,
        result_message_array
    )
    
    nowtime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
    user_profile_dict = vars(user_profile)
    print(user_profile_dict,
        user_profile_dict.get("display_name"),
        user_profile_dict.get("picture_url"),
        user_profile_dict.get("status_message"),
        user_profile_dict.get("user_id"),
        nowtime
    )
    

# In[5]:


'''

handler處理文字消息

收到用戶回應的文字消息，
按文字消息內容，往素材資料夾中，找尋以該內容命名的資料夾，讀取裡面的reply.json

轉譯json後，將消息回傳給用戶

'''

# 引用套件
from linebot.models import (
    MessageEvent, TextMessage
)
import os
import redis, datetime

#引用副程式
import app_1_news, Msg_Template, stockprice, kchart, Technical_Analysis, Institutional_Investors
emoji_upinfo = u'\U0001F447'

# 文字消息處理
@handler.add(MessageEvent,message=TextMessage)
def process_text_message(event):
    
    nowtime = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    msg = str(event.message.text).upper().strip()
    # 取出消息內User的資料
    profile = line_bot_api.get_profile(event.source.user_id)
#     print(profile)
     
    #取出userid, displayname 丟回全域變數
    profile_dict = vars(profile)    
    print("使用者輸入內容 =", msg, " ,LINE名字 =", profile_dict.get("display_name"), " ,使用者 =", profile_dict.get("user_id"), " ,輸入內容時間 =", nowtime)
            
    ID = profile_dict.get("user_id")#
    text = event.message.text  #
    query = str(text)  #
    groupid = str(ID)  #

        
        
    if msg == '.2-1_10%內可接受範圍':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您喜愛以小博大!\n建議您可以選擇如下:\n1.定存。\n2.政府公債。\n3.保本型基金。'))
        
    elif msg == '.2-3_50%內可接受範圍':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您極端厭惡風險!\n建議您可以選擇如下:\n1.權證。\n2.期貨。\n3.選擇權。\n4.對沖基金。\n5.股票型基金。'))
    
    elif msg == '.2-4_100%以上':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您賭性堅強!\n給予您以下建議:\n小賭怡情，大賭亂性。\n能戒則戒。\n靠勞力所得，\n雖少，\n但很實在。'))
        
    elif msg == '.3-1_1個月內':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您過高期待!\n給予您以下建議:\n自行創業。\n雖初期辛苦，\n但只要熬過去，\n報酬率會超過\n您在股市所得。'))
        
    elif msg == '.3-4_1年以上':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您喜愛被動投資!\n建議您可以選擇如下:\n1.ETF。\n不用想了，\n就是上面那選擇。'))
        
    elif msg == '.4-1_每天花費1~2小時':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您賭性堅強!\n給予您以下建議:\n小賭怡情，大賭亂性。\n能戒則戒。\n靠勞力所得，\n雖少，\n但很實在。'))
        
    elif msg == '.4-3_每月花費1~2小時':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您追求"穩定"!\n建議您可以選擇如下:\n1.定存。\n2.儲蓄險。'))
        
    elif msg == '.5-1_高風險高報酬':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您過高期待!\n給予您以下建議:\n自行創業。\n雖初期辛苦，\n但只要熬過去，\n報酬率會超過\n您在股市所得。'))
        
    elif msg == '.6-1_投資一定有風險':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您喜愛被動投資!\n建議您可以選擇如下:\n1.ETF。\n不用想了，\n就是上面那選擇。'))
        
    elif msg == '.7-1_我很積極布局':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您是高級打工仔!\n建議您可以選擇如下:\n1.當沖交易。\n基本條件:A.資本要大，\nB.本身操作能力優秀。'))

    elif msg == '.7-2_我要觀察一陣子':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您統計學優秀!\n建議您可以選擇如下:\n1.權證。\n2.期貨。\n3.選擇權。\n4.股票。'))

    elif msg == '.7-4_認賠殺出':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您喜愛被動投資!\n建議您可以選擇如下:\n1.ETF。\n不用想了，\n就是上面那選擇。'))

    elif msg == '.8-1_我喜愛賺價差':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您很有耐心!\n建議您可以選擇如下:\n您選擇的股票商品，\n低點進場，\n高點賣出，\n您有您的投資方式。'))

    elif msg == '.8-2_我喜愛超高報酬':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好，\n我猜測您眼光很準!\n建議您可以選擇如下:\n美股，\n能達到您心中所想，\n投資多年，\n股價越爬越高。'))
    
    # 個股新聞
    elif re.match('N[0-9]{4}', msg):  
        stockNumber = msg[1:5]
        content = app_1_news.single_stock(stockNumber)
        line_bot_api.reply_message(event.reply_token, TextSendMessage('即將給您編號' + stockNumber + '\n個股新聞!'))
        line_bot_api.push_message(ID, content)
        btn_msg = Msg_Template.stock_reply_other_news(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    # 每週新聞回顧
    elif re.match("每週新聞回顧", msg):
        line_bot_api.push_message(ID, TextSendMessage("我們將給您最新的周回顧，\n請點選圖片連結!!"))
        line_bot_api.push_message(ID, app_1_news.weekly_finance_news())
    
    # 查詢某檔股票開高收低價格
    elif re.match('S[0-9]', msg):  
        stockNumber = msg[1:]
        stockName = stockprice.get_stock_name(stockNumber)
        if stockName == "no":
            line_bot_api.push_message(ID, TextSendMessage("股票編號錯誤"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('稍等一下,\n查詢編號' + stockNumber + '\n的資訊中...'))
            content_text = stockprice.getprice(stockNumber, msg)
            content = Msg_Template.stock_reply_other_price(stockNumber, content_text)
            line_bot_api.push_message(ID, content)
    
    #原K線圖     #OK
#     elif re.match("K[0-9]{4}", msg):
#         stockNumber = msg[1:]
#         content = Msg_Template.kchart_msg + "\n" + Msg_Template.kd_msg
#         line_bot_api.push_message(ID, TextSendMessage(content))
#         line_bot_api.push_message(ID, TextSendMessage('稍等一下,\nK線圖繪製中...'))
#         k_imgurl = kchart.draw_kchart(stockNumber)
#         line_bot_api.push_message(ID, ImageSendMessage(original_content_url=k_imgurl, preview_image_url=k_imgurl))
#         btn_msg = Msg_Template.stock_reply_other_K(stockNumber)
#         line_bot_api.push_message(ID, btn_msg)
    
    #原MACD指標     #OK
#     elif re.match("MACD[0-9]", msg):
#         stockNumber = msg[4:]
#         content = Msg_Template.macd_msg
#         line_bot_api.push_message(ID, TextSendMessage('稍等一下,\n將給您編號' + stockNumber + '\nMACD指標...'))
#         line_bot_api.push_message(ID, TextSendMessage(content))
#         MACD_imgurl = Technical_Analysis.MACD_pic(stockNumber, msg)
#         line_bot_api.push_message(ID,
#             ImageSendMessage(original_content_url=MACD_imgurl, preview_image_url=MACD_imgurl))
#         btn_msg = Msg_Template.stock_reply_other_MACD(stockNumber)
#         line_bot_api.push_message(ID, btn_msg)
    
    #RSI指標  #OK
    elif re.match('RSI[0-9]', msg):
        stockNumber = msg[3:]
        line_bot_api.push_message(ID, TextSendMessage('稍等一下,\n將給您編號' + stockNumber + '\nRSI指標...'))
        RSI_imgurl = Technical_Analysis.stock_RSI(stockNumber)
        line_bot_api.push_message(ID, ImageSendMessage(original_content_url=RSI_imgurl, preview_image_url=RSI_imgurl))
        btn_msg = Msg_Template.stock_reply_other_RSI(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    #BBAND指標      #OK
    elif re.match("BBAND[0-9]", msg):
        stockNumber = msg[5:]
        content = Msg_Template.bband_msg
        line_bot_api.push_message(ID, TextSendMessage(content))
        line_bot_api.push_message(ID, TextSendMessage('稍等一下,\n將給您編號' + stockNumber + '\nBBand指標...'))
        BBANDS_imgurl = Technical_Analysis.BBANDS_pic(stockNumber, msg)
        line_bot_api.push_message(ID,
            ImageSendMessage(original_content_url=BBANDS_imgurl, preview_image_url=BBANDS_imgurl))
        btn_msg = Msg_Template.stock_reply_other_BBAND(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    #畫近一年股價走勢圖      #OK
    elif re.match("P[0-9]{4}", msg):
        stockNumber = msg[1:]
        line_bot_api.push_message(ID, TextSendMessage('稍等一下,\n將給您編號' + stockNumber + '\n股價走勢圖!'))
        trend_imgurl = stockprice.stock_trend(stockNumber, msg)
        line_bot_api.push_message(ID,
            ImageSendMessage(original_content_url=trend_imgurl, preview_image_url=trend_imgurl))
        btn_msg = Msg_Template.stock_reply_other_P(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    # 個股年收益率分析圖 #OK
    elif re.match('E[0-9]{4}', msg):
        targetStock = msg[1:]
        line_bot_api.push_message(ID, TextSendMessage('分析' + targetStock + '中，\n年收益率圖產生中，\n稍等一下。'))
        imgurl2 = stockprice.show_return(targetStock, msg)  
        line_bot_api.push_message(ID, ImageSendMessage(original_content_url=imgurl2, preview_image_url=imgurl2))
        btn_msg = Msg_Template.stock_reply_other_E(targetStock)
        line_bot_api.push_message(ID, btn_msg)
    
    #三大法人買賣資訊  #OK
    elif re.match('F[0-9]', msg):
        stockNumber = msg[1:]
        line_bot_api.push_message(ID, TextSendMessage('稍等一下,\n將給您編號' + stockNumber + '\n三大法人買賣資訊...'))
        content = Institutional_Investors.institutional_investors(stockNumber)
        line_bot_api.push_message(ID, TextSendMessage(content))
        btn_msg = Msg_Template.stock_reply_other_F(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    # 籌碼面分析圖    #失敗_有空從做此步
#     elif re.match('C[0-9]', msg):
#         targetStock = msg[1:]
#         line_bot_api.push_message(ID, TextSendMessage('分析' + targetStock + '中，\n籌碼面分析圖產生中，\n稍等一下。'))
#         imgurl2 = Institutional_Investors.institutional_investors_pic(targetStock)
#         if imgurl2 == "股票代碼錯誤!":
#             line_bot_api.push_message(ID, TextSendMessage("股票代碼錯誤!"))
        
#         line_bot_api.push_message(ID, ImageSendMessage(original_content_url=imgurl2, preview_image_url=imgurl2))
#         btn_msg = Msg_Template.stock_reply_other(targetStock)
#         line_bot_api.push_message(ID, btn_msg)
    
    #功能說明
    elif msg == '功能說明':
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好～\n在此說明我的功能!\n\nK+個股代號(舉例:K2330)，\n=>會產生出2330的K線圖。\n\nN+個股代號(舉例:N2330)，\n=>會顯示近期2330的新聞連結。\n\nS+個股代號(舉例:S2330)，\n=>會顯示最近2330的\n開、高、收、低價格。\n\nMACD+個股代號(舉例:MACD2330)，\n=>會產生出2330的MACD指標圖。\n\nRSI+個股代號(舉例:RSI2330)，\n=>會產生出2330的RSI指標圖。\n\nBBAND+個股代號(舉例:BBAND2330)，\n=>會產生出2330的BBAND指標圖。\n\nP+個股代號(舉例:P2330)，\n=>會產生出2330的一年股價走勢圖。\n\nE+個股代號(舉例:E2330)，\n=>會產生出2330的年收益率分析圖。\n\nF+個股代號(舉例:F2330)，\n=>會產生出2330三大法人買賣資訊。\n\n功能說明完畢，\n謝謝觀看!!'))
    
        #K_line_0718線圖     #OK
    elif re.match("K[0-9]{4}", msg):
        stockNumber = msg[1:]
        content = Msg_Template.kchart_msg + "\n" + Msg_Template.kd_msg
        line_bot_api.reply_message(event.reply_token, TextSendMessage(content))
        line_bot_api.push_message(ID, TextSendMessage('稍等一下,\nK線圖繪製中...'))
        k_imgurl = kchart.K_line_0721(stockNumber)
        line_bot_api.push_message(ID, ImageSendMessage(original_content_url=k_imgurl, preview_image_url=k_imgurl))
        btn_msg = Msg_Template.stock_reply_other_K(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    #MACD_0718線圖
    elif re.match("MACD[0-9]", msg):
        stockNumber = msg[4:]
        content = Msg_Template.macd_msg
        line_bot_api.reply_message(event.reply_token, TextSendMessage('稍等一下,\n將給您編號' + stockNumber + '\nMACD指標...'))
        line_bot_api.push_message(ID, TextSendMessage(content))
        MACD_imgurl = Technical_Analysis.MMACD_pic(stockNumber, msg)
        line_bot_api.push_message(ID,
            ImageSendMessage(original_content_url=MACD_imgurl, preview_image_url=MACD_imgurl))
        btn_msg = Msg_Template.stock_reply_other_MACD(stockNumber)
        line_bot_api.push_message(ID, btn_msg)
    
    #問候語回應
    elif msg in ("你好", "哈嘍", 'HI', 'hi', '嗨', "妳好", "您好", "Hi", "hI"):
        line_bot_api.reply_message(event.reply_token, \
            TextSendMessage(text='您好～歡迎加入股市小子!\n下方圖文選單可以點選!\n或請點選下方"功能說明"，\n會詳列出我的功能說明!'))
    

    else:
        pass 


    # 讀取本地檔案，並轉譯成消息
    result_message_array =[]
    replyJsonPath = "素材/"+event.message.text+"/reply.json"
    result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
    
    # 發送
    line_bot_api.reply_message(
    event.reply_token,
    result_message_array
    )

# In[6]:


'''

handler處理Postback Event

載入功能選單與啟動特殊功能

解析postback的data，並按照data欄位判斷處理

現有三個欄位
menu, folder, tag

若folder欄位有值，則
    讀取其reply.json，轉譯成消息，並發送

若menu欄位有值，則
    讀取其rich_menu_id，並取得用戶id，將用戶與選單綁定
    讀取其reply.json，轉譯成消息，並發送

'''
from linebot.models import (
    PostbackEvent
)

from urllib.parse import parse_qs 

@handler.add(PostbackEvent)
def process_postback_event(event):
    
    query_string_dict = parse_qs(event.postback.data)
    
    print(query_string_dict)
    if 'folder' in query_string_dict:
    
        result_message_array =[]

        replyJsonPath = '素材/'+query_string_dict.get('folder')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )
    elif 'menu' in query_string_dict:
 
        linkRichMenuId = open("素材/"+query_string_dict.get('menu')[0]+'/rich_menu_id', 'r').read()
        line_bot_api.link_rich_menu_to_user(event.source.user_id,linkRichMenuId)
        
        replyJsonPath = '素材/'+query_string_dict.get('menu')[0]+"/reply.json"
        result_message_array = detect_json_array_to_new_message_array(replyJsonPath)
  
        line_bot_api.reply_message(
            event.reply_token,
            result_message_array
        )


# In[ ]:


'''

Application 運行（開發版）

'''
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')


# In[ ]:


'''

Application 運行（heroku版）

'''



if __name__ == "__main__":

    app.run(host='0.0.0.0',port=os.environ['PORT'])


# In[ ]:




