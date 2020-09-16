import pandas as pd
import matplotlib
matplotlib.use('Agg')
# import talib
from talib import abstract
import Imgur
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import requests
from bs4 import BeautifulSoup
from matplotlib.font_manager import FontProperties # 設定字體
chinese_font = matplotlib.font_manager.FontProperties(fname='msjh.ttf') # 引入同個資料夾下支援中文字檔

def general_df(stockNumber):
    stockNumberTW  =  stockNumber + ".TW"
    df_x=pdr.DataReader(stockNumberTW,'yahoo',start="2019")
    df_x.rename(columns = {'Open':'open', 'High':'high', 'Low':'low', 'Close':'close'}, inplace = True)
    return df_x

def get_stockName(stockNumber):
    url = 'https://tw.stock.yahoo.com/q/q?s='+stockNumber
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all(text='成交')[0].parent.parent.parent
    stock_name = table.select('tr')[1].select('td')[0].text
    stock_name = stock_name.strip('加到投資組合')
    return stock_name

def MACD_pic(stockNumber, msg):
    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    jj=df_x.reset_index(drop=False)
    abstract.MACD(df_x).plot(figsize=(16,8))
    plt.xlabel("date",  FontProperties=chinese_font)
    plt.ylabel("Value",  FontProperties=chinese_font)
    plt.grid(True,axis='y')
    plt.title(stock_name+"MACD線" ,FontProperties=chinese_font)
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgurMACD(msg)

# ===================================
# KD指標
def RSI_pic(stockNumber, msg):
    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    jj=df_x.reset_index(drop=False)
    abstract.RSI(df_x).plot(figsize=(16,8))
    plt.xlabel("date",  FontProperties=chinese_font)
    plt.ylabel("KD值",  FontProperties=chinese_font)
    plt.grid(True,axis='y')
    plt.title(stock_name+"KD線" ,FontProperties=chinese_font)
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgur(msg)

# ===================================
# BBand分析
def BBANDS_pic(stockNumber, msg):
    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    jj=df_x.reset_index(drop=False)
    abstract.BBANDS(df_x).plot(figsize=(16,8))
    plt.xlabel("date",  FontProperties=chinese_font)
    plt.ylabel("價格",  FontProperties=chinese_font)
    plt.grid(True,axis='y')
    plt.title(stock_name+"BBANDS" ,FontProperties=chinese_font)
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgurBBAND(msg)



from pandas_datareader import data
import yfinance as yf # yahoo專用的拿來拉股票資訊
import datetime
import talib #技術分析專用
import mpl_finance as mpf # 專門用來畫蠟燭圖的
pd.core.common.is_list_like = pd.api.types.is_list_like
#設定顏色
color=['#2196f3','#4caf50','#ffc107','#f436c7','#f27521','#e00b0b']

def TheConstructor(userstock):
    # 設定要的資料時間
    start = datetime.datetime.now() - datetime.timedelta(days=365) #先設定要爬的時間
    end = datetime.date.today()
    
    # 與yahoo請求
    pd.core.common.is_list_like = pd.api.types.is_list_like
    yf.pdr_override()
    
    # 取得股票資料
    try:
        stock = data.get_data_yahoo(userstock+'.TW', start, end)

    except :
        # 如果失敗回傳"失敗"這張圖
        stock = 'https://i.imgur.com/RFmkvQX.jpg'
        
    return stock

#------------------------ 相對強弱指數（Relative Strength Index）------------------------------------
def stock_RSI(userstock):
    stock=TheConstructor(userstock)
    if type(stock) == str:
        return stock
    else:
        # RSI的天數設定一般是6, 12, 24
        ret = pd.DataFrame(talib.RSI(stock['Close'],6), columns= ['Relative Strength Index'])
        ret = pd.concat([ret,stock['Close']], axis=1)
        
        ### 開始畫圖 ###
        ret.plot(color=color, linestyle='dashed')
        ret['Close'].plot(secondary_y=True,color=color[5])
        plt.title(userstock + 'RSI') # 標題設定
        plt.grid(True,axis='y')
        plt.show()
        plt.savefig('Relative_Strength_Index.png') #存檔
        plt.close() # 刪除記憶體中的圖片
        return Imgur.showImgurRSI('Relative_Strength_Index')
# stock_RSI("2330")



#MMACD
def MMACD_pic(stockNumber, msg):

    stock_name = get_stockName(stockNumber)
    df_x = general_df(stockNumber)
    df_raw = df_x.reset_index()
    df_raw['Date'] = df_raw['Date'].dt.date
    scale = 240
    df_raw = df_raw[-scale:]
    fast_ewm = df_raw['close'].ewm(span=12).mean()
    slow_ewm = df_raw['close'].ewm(span=26).mean()

    dif = fast_ewm - slow_ewm
    dea = dif.ewm(span=9).mean()

    bar = (dif - dea) * 2

    red_bar = bar[bar >= 0]
    green_bar = bar[bar < 0]
    dpi = 72
    canvas_w = 1000
    canvas_h = 480
    figsize = canvas_w / 72, canvas_h / 72
    plt.figure(figsize=figsize)

    p_dif = plt.plot(dif.index, dif.values)
    p_dea = plt.plot(dea.index, dea.values)
    plt.bar(red_bar.index, red_bar.values, color='#d62728')
    plt.bar(green_bar.index, green_bar.values, color='#889966')
    xtick_period = 30
    major_index = df_raw.index[df_raw.index % xtick_period == 20]
    major_xtics = df_raw['Date'][df_raw.index % xtick_period == 20]
    plt.xticks(major_index, major_xtics)
    plt.legend((p_dif[0], p_dea[0]), [u'DIF', u'DEA'])
    plt.title(stockNumber + '_MACD', fontproperties=chinese_font)
    plt.show
    plt.savefig(msg + ".png")
    plt.close()
    return Imgur.showImgurMACD(msg)

