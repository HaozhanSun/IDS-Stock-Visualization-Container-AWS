import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

def save_tickers():
    resp=requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup=bs.BeautifulSoup(resp.text)
    table=soup.find('table',{'class':'wikitable sortable'})
    tickers=[]
    for row in table.findAll('tr')[1:]:
        ticker=row.findAll('td')[0].text[:-1]
        tickers.append(ticker)
    with open("tickers.pickle",'wb') as f:
        pickle.dump(tickers, f)
    return tickers
save_tickers()


def fetch_data():
    with open("tickers.pickle",'rb') as f:
        tickers=pickle.load(f)
    if not os.path.exists('stock_details'):
        os.makedirs('stock_details')
    count=200
    start= dt.datetime(2010,1,1)
    end=dt.datetime(2020,6,22)
    count=0
    for ticker in tickers:
        if count==200:
            break
        count+=1

        try:
            df=web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_details/{}.csv'.format(ticker))
        except:
            print("Error")
            continue
fetch_data()

def compile():
    with open("tickers.pickle",'rb') as f:
        tickers=pickle.load(f)
    main_df=pd.DataFrame()

    for count,ticker in enumerate(tickers):
        if 'AMZN' in ticker:
            continue
        if not os.path.exists('stock_details/{}.csv'.format(ticker)):
            continue
        df=pd.read_csv('stock_details/{}.csv'.format(ticker))
        df.set_index('Date',inplace=True)

    df.rename(columns={'Adj Close': ticker}, inplace=True)
    df.drop(['Open','High','Low',"Close",'Volume'],axis=1,inplace=True)

    if main_df.empty:
        main_df=df
    else:
        main_df=main_df.join(df,how='outer')

    print(main_df.head())
    main_df.to_csv('Dataset_temp.csv')
compile()

df=pd.read_csv('stock_details/AMZN.csv',index_col=0,parse_dates=True)
df_ohlc= df['Adj Close'].resample('10D').ohlc()
df_volume=df['Volume'].resample('10D').sum()
df_ohlc.reset_index(inplace=True)
df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)
plt.figure(figsize=(15, 9))
ax1=plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2=plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1 , sharex=ax1)
ax1.xaxis_date()
candlestick_ohlc(ax1,df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)
plt.show()