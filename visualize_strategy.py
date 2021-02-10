import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import talib
import alpaca_trade_api as tradeapi
import pandas as pd

from common import load_yaml

# Load env variables
ENV = load_yaml("env.yaml")
KEY_ID = ENV["key_id"]
SECRET_KEY = ENV["secret_key"]

# Instantiate alpaca_trade_api
TRADE_API = tradeapi.REST(key_id=KEY_ID, secret_key=SECRET_KEY)

# Set variables
assets_to_download = ["SPY","MSFT","AAPL","NFLX"]
barTimeframe = "1D" # 1Min, 5Min, 15Min, day or 1D. minute
NY = 'America/New_York'
startDate = pd.Timestamp('2020-01-01', tz=NY).isoformat()

for symbol in assets_to_download:
    returned_data = TRADE_API.get_barset(symbol, barTimeframe, start=startDate).df

    timeList = returned_data.index.strftime('%Y-%m-%dT%H:%M:%SZ')
    openList = returned_data.iloc[:,0].values.tolist()
    highList = returned_data.iloc[:,1].values.tolist()
    lowList = returned_data.iloc[:,2].values.tolist()
    closeList = returned_data.iloc[:,3].values.tolist()
    volumeList = returned_data.iloc[:,4].values.tolist()

    # # Reads, formats and stores the new bars
    # for bar in returned_data.iterrows():
    #     print(bar)
    #     timeList.append(datetime.strptime(bar.time,'%Y-%m-%dT%H:%M:%SZ'))
    #     openList.append(bar.open)
    #     highList.append(bar.high)
    #     lowList.append(bar.low)
    #     closeList.append(bar.close)
    #     volumeList.append(bar.volume)
	
    # Processes all data into numpy arrays for use by talib
    timeList = np.array(timeList)
    openList = np.array(openList,dtype=np.float64)
    highList = np.array(highList,dtype=np.float64)
    lowList = np.array(lowList,dtype=np.float64)
    closeList = np.array(closeList,dtype=np.float64)
    volumeList = np.array(volumeList,dtype=np.float64)

    # Calculated trading indicators
    SMA20 = talib.SMA(closeList,20)
    SMA50 = talib.SMA(closeList,50)


    # Defines the plot for each trading symbol
    f, ax = plt.subplots()
    f.suptitle(symbol)

    # Plots market data and indicators
    ax.plot(timeList,closeList,label=symbol,color="black")
    ax.plot(timeList,SMA20,label="SMA20",color="green")
    ax.plot(timeList,SMA50,label="SMA50",color="red")

    # Fills the green region if SMA20 > SMA50 and red if SMA20 < SMA50
    ax.fill_between(timeList, SMA50, SMA20, where=SMA20 >= SMA50, facecolor='green', alpha=0.5, interpolate=True)
    ax.fill_between(timeList, SMA50, SMA20, where=SMA20 <= SMA50, facecolor='red', alpha=0.5, interpolate=True)

    # Adds the legend to the right of the chart
    ax.legend(loc='center left', bbox_to_anchor=(1.0,0.5))

plt.show()