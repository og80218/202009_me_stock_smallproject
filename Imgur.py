'''
上傳圖片
'''

import matplotlib
matplotlib.use('Agg')
# import datetime
# from imgurpython import ImgurClient
from os import path
from imgur_python import Imgur

# 載入json處理套件
import json, re, sys

# 載入基礎設定檔
secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))

client_id = secretFileContentJson.get("imgur_API_client_id")                                          
client_secret = secretFileContentJson.get("imgur_API_client_secret")              
album_id = secretFileContentJson.get("imgur_album_id")                                                            
access_token = secretFileContentJson.get("Postman_access_token")     
refresh_token = secretFileContentJson.get("Postman_refresh_token")    

#pin code:40ea90b2dc

#BBAND指標
# fileName = 'BBAND'+'[0-9]'
def showImgurBBAND(fileName):
        imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})

        # 開始上傳檔案
        try:
            # print("[log:INFO]Uploading image... ")
            imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled', 'My first image upload')
            image_id = imgurla['response']['data']['id']
            #string to dict
            print("[log:INFO]Done upload. ")
            # print(imgurl)
            imgurl = 'https://i.imgur.com/' + image_id + '.png'
        except :
            # 如果失敗回傳"失敗"這張圖
            imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
            print("[log:ERROR]Unable upload ! ")

        return imgurl

#存K線圖
# fileName = 'Kchrat'
def showImgurK(fileName):
    imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})

    # 開始上傳檔案
    try:
        # print("[log:INFO]Uploading image... ")
        imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled', 'My first image upload')
        image_id = imgurla['response']['data']['id']
        # string to dict
        print("[log:INFO]Done upload. ")
        # print(imgurl)
        imgurl = 'https://i.imgur.com/' + image_id + '.png'
    except:
        # 如果失敗回傳"失敗"這張圖
        imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
        print("[log:ERROR]Unable upload ! ")

    return imgurl

# fileName = 'C' + '[0-9]'      法人
def showImgurC(fileName):
    imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})

    # 開始上傳檔案
    try:
        # print("[log:INFO]Uploading image... ")
        imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled',
                                            'My first image upload')
        image_id = imgurla['response']['data']['id']
        # string to dict
        print("[log:INFO]Done upload. ")
        # print(imgurl)
        imgurl = 'https://i.imgur.com/' + image_id + '.png'
    except:
        # 如果失敗回傳"失敗"這張圖
        imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
        print("[log:ERROR]Unable upload ! ")

    return imgurl

# fileName = 'MACD' + '[0-9]'
def showImgurMACD(fileName):
    imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})

    # 開始上傳檔案
    try:
        # print("[log:INFO]Uploading image... ")
        imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled',
                                            'My first image upload')
        image_id = imgurla['response']['data']['id']
        # string to dict
        print("[log:INFO]Done upload. ")
        # print(imgurl)
        imgurl = 'https://i.imgur.com/' + image_id + '.png'
    except:
        # 如果失敗回傳"失敗"這張圖
        imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
        print("[log:ERROR]Unable upload ! ")

    return imgurl

# fileName = '一年股價走勢圖' + '[0-9]'
def showImgurP(fileName):
    imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})
    # 開始上傳檔案
    try:
        # print("[log:INFO]Uploading image... ")
        imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled',
                                            'My first image upload')
        image_id = imgurla['response']['data']['id']
        # string to dict
        print("[log:INFO]Done upload. ")
        # print(imgurl)
        imgurl = 'https://i.imgur.com/' + image_id + '.png'
    except:
        # 如果失敗回傳"失敗"這張圖
        imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
        print("[log:ERROR]Unable upload ! ")

    return imgurl


# fileName = 'RSI' + '[0-9]'
def showImgurRSI(fileName):
    imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})

    # 開始上傳檔案
    try:
        # print("[log:INFO]Uploading image... ")
        imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled',
                                            'My first image upload')
        image_id = imgurla['response']['data']['id']
        # string to dict
        print("[log:INFO]Done upload. ")
        # print(imgurl)
        imgurl = 'https://i.imgur.com/' + image_id + '.png'
    except:
        # 如果失敗回傳"失敗"這張圖
        imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
        print("[log:ERROR]Unable upload ! ")

    return imgurl

# fileName = '收益率' + '[0-9]'
def showImgurS(fileName):
    imgur_client = Imgur({'client_id': client_id, 'access_token': access_token})

    # 開始上傳檔案
    try:
        # print("[log:INFO]Uploading image... ")
        imgurla = imgur_client.image_upload(path.realpath('./' + fileName + '.png'), 'Untitled',
                                            'My first image upload')
        image_id = imgurla['response']['data']['id']
        # string to dict
        print("[log:INFO]Done upload. ")
        # print(imgurl)
        imgurl = 'https://i.imgur.com/' + image_id + '.png'
    except:
        # 如果失敗回傳"失敗"這張圖
        imgurl = 'https://i.imgur.com/RFmkvQX.jpg'
        print("[log:ERROR]Unable upload ! ")

    return imgurl