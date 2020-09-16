# basic
import numpy as np
# import pandas as pd
import Imgur
# get data
# import pandas_datareader as pdr

# visual
import matplotlib
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas_datareader as pdr
# import seaborn as sns
from bs4 import BeautifulSoup
#time
# import datetime as datetime

#talib
import talib
# import pandas as pd
import requests,datetime
from matplotlib.font_manager import FontProperties # 設定字體
chinese_font = matplotlib.font_manager.FontProperties(fname='msjh.ttf') # 引入同個資料夾下支援中文字檔
chinese_title = matplotlib.font_manager.FontProperties(fname='msjh.ttf', size=24) # 引入同個資料夾下支援中文字檔
chinese_subtitle = matplotlib.font_manager.FontProperties(fname='msjh.ttf', size=20) # 引入同個資料夾下支援中文字檔

def get_stock_name(stockNumber):
    try:
        url = 'https://tw.stock.yahoo.com/q/q?s=' + stockNumber
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all(text='成交')[0].parent.parent.parent
        stock_name = table.select('tr')[1].select('td')[0].text.strip('加到投資組合')
        return stock_name
    except:
        return "no"


def draw_kchart(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock.index = stock.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    #KD
    sma_10 = talib.SMA(np.array(stock['Close']), 10)
    sma_30 = talib.SMA(np.array(stock['Close']), 30)
    stock['k'], stock['d'] = talib.STOCH(stock['High'], stock['Low'], stock['Close'])
    stock['k'].fillna(value=0, inplace=True)
    stock['d'].fillna(value=0, inplace=True)
    sma_5 = talib.SMA(np.array(stock['Close']), 5)
    sma_20 = talib.SMA(np.array(stock['Close']), 20)
    sma_60 = talib.SMA(np.array(stock['Close']), 60)
    fig = plt.figure(figsize=(20, 10))#,facecolor='black')
    fig.suptitle(stock_name.strip('加到投資組合'),fontsize="x-large", FontProperties=chinese_title)
    ax = fig.add_axes([0.1,0.5,0.75,0.4])
    plt.title("開盤價:"+str(round(stock['Open'][-1], 2))+"  收盤價:"+str(round(stock['Close'][-1], 2))+"\n最高價:"+str(round(stock['High'][-1] ,2))+"  最低價:"+str(round(stock['Low'][-1], 2)),fontsize="25",fontweight='bold',bbox=dict(facecolor='yellow',edgecolor='red',alpha=0.65),loc='left', FontProperties=chinese_subtitle)
    plt.title("更新日期:"+stock.index[-1],fontsize="20",fontweight='bold',loc="right", FontProperties=chinese_subtitle)
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')

    ax2 = fig.add_axes([0.1,0.3,0.75,0.20])
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    ax3 = fig.add_axes([0.1,0.03,0.75,0.20])
    mpf.candlestick2_ochl(ax, stock['Open'], stock['Close'], stock['High'],
                      stock['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
    ax.plot(sma_5, label='5日均線')
    ax.plot(sma_10, label='10日均線')
    ax.plot(sma_20, label='20日均線')
    ax.plot(sma_60, label='60日均線')

    ax2.plot(stock['k'], label='K值')
    ax2.plot(stock['d'], label='D值')

    ax2.set_xticks(range(0, len(stock.index),10))
    ax2.set_xticklabels(stock.index[::10],fontsize="10", rotation=25)

    mpf.volume_overlay(ax3, stock['Open'], stock['Close'], stock['Volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
    ax3.set_xticks(range(0, len(stock.index),10))
    ax3.set_xticklabels(stock.index[::5],fontsize="10", rotation=45)

    ax.legend(prop=chinese_font, fontsize=20);
    ax2.legend(prop=chinese_font);
    plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')
    plt.gcf()
    plt.savefig("Kchrat.png",bbox_inches='tight',dpi=300,pad_inches=0.0)
    plt.show()
    plt.close()
    return Imgur.showImgurK("Kchrat")

def K_line_0721(stockNumber):
    stock_name = get_stock_name(stockNumber)
    if stock_name == "no": return "股票代碼錯誤!"
    end = datetime.datetime.now()
    date = end.strftime("%Y%m%d")
    year = str(int(date[0:4]) - 1)
    month = date[4:6]
    stock = pdr.DataReader(stockNumber + '.TW', 'yahoo', start= year+"-"+month,end=end)
    stock.index = stock.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    #KD
    # 畫圖的資料量
    stockNumber = str(stockNumber)
    scale = 240
    stock = stock[-scale:]
    # 創fig
    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(17, 10))
    plt.subplots_adjust(hspace=0.5)

    #plt.title("開盤價:" + str(round(stock['Open'][-1], 2)) + "  收盤價:" + str(round(stock['Close'][-1], 2)) + "\n最高價:" + str(
#         round(stock['High'][-1], 2)) + "  最低價:" + str(round(stock['Low'][-1], 2)),
#               fontsize="25", fontweight='bold', bbox=dict(facecolor='crimson'
#                                                           , edgecolor='white', alpha=0.65), loc='center',
#               FontProperties=chinese_subtitle)

    plt.title("更新日期:" + str(stock.index[-1]), fontsize="20", fontweight='bold', loc="right", FontProperties=chinese_subtitle)

    # 畫K線(蠟燭線)
    mpf.candlestick2_ochl(ax1, stock.Open, stock.Close, stock.High, stock.Low, width=0.5,
                          colorup='r', colordown='g')
    # 最高價,最低價,當日開盤價,當日收盤價


    # plt.title("Date:"+b.index[-1],fontsize="20",fontweight='bold',loc="right")
    # 畫移動平均線
    # pd.rolling_mean(df_stockload.Close,window=20)
    stock['Ma5'] = stock.Close.rolling(window=5).mean()

    # pd.rolling_mean(df_stockload.Close,window=30)
    stock['Ma10'] = stock.Close.rolling(window=10).mean()

    # pd.rolling_mean(df_stockload.Close,window=30)
    stock['Ma20'] = stock.Close.rolling(window=20).mean()

    # pd.rolling_mean(df_stockload.Close,window=60)
    stock['Ma60'] = stock.Close.rolling(window=60).mean()

    # plt.grid(True,linestyle="--",color='gray',linewidth='0.5',axis='both')


    # 放置圖例
    ax1.plot(np.arange(0, len(stock.index)), stock['Ma5'], 'deeppink', label='5日均線', lw=0.5)
    ax1.plot(np.arange(0, len(stock.index)), stock['Ma10'], 'orange', label='10日均線', lw=0.5)
    ax1.plot(np.arange(0, len(stock.index)), stock['Ma20'], 'green', label='20日均線', lw=0.5)
    ax1.plot(np.arange(0, len(stock.index)), stock['Ma60'], 'blue', label='60日均線', lw=0.5)

    # 標示當天日期

    ax1.legend(loc='best',prop=chinese_font)
    ax1.set_title(stockNumber + "_K_Line")
    ax1.set_xlabel("date")
    ax1.set_ylabel("price")
    # ax1.set_xlim(0, len(b.index))  # 設定X軸範圍
    ax1.set_xticks(range(0, len(stock.index), 15))  # 以15天為單位,標示日期
    ax1.set_xticklabels([stock.index[index] for index in ax1.get_xticks()])  # 設定X軸為日期
    # 繪製K、D線圖
#     stock['k'], stock['d'] = talib.STOCH(stock['High'], stock['Low'], stock['Close'])
#     stock['k'].fillna(value=0, inplace=True)
#     stock['d'].fillna(value=0, inplace=True)
    
#     ax2 = fig.add_axes([0.1,0.3,0.75,0.20])

#     ax2.plot(stock['k'], label='K值')
#     ax2.plot(stock['d'], label='D值')

#     ax2.set_xticks(range(0, len(stock.index),10))
#     ax2.set_xticklabels(stock.index[::10],fontsize="10", rotation=45)
#     ax2.legend(prop=chinese_font);
    # 繪製成交量子圖

    mpf.volume_overlay(ax3, stock['Open'], stock['Close'], stock['Volume'], colorup='red', colordown='green', width=1.0, alpha=0.8)
    ax3.set_xticks(range(0, len(stock.index), 15))
    ax3.set_xticklabels([stock.index[index] for index in ax3.get_xticks()])
    ax3.set_xticklabels(stock.index[::5], fontsize="8", rotation=25)

    # 使日期傾斜以供辨識
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(25)
        label.set_fontsize(10)
        
    plt.gcf()
    plt.savefig("Kchrat.png",bbox_inches='tight',dpi=300,pad_inches=0.0)
    plt.show()
    plt.close()
    return Imgur.showImgurK("Kchrat")