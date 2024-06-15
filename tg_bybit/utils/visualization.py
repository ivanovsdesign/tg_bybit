import matplotlib.pyplot as plt
import io
from datetime import datetime
import numpy as np

def generate_plot(data: dict,
                  pair: str) -> io.BytesIO:
    '''
    Generates plot based on trading data
    '''
    times = [datetime.fromtimestamp(int(candle[0]) / 1000) for candle in data['result']['list']]
    closes = [float(candle[4]) for candle in data['result']['list']]

    x = np.linspace(0,100,100)
    y = [2 * k for k in x]

    # plt.plot(x, y)
    # buf = io.BytesIO()
    # plt.savefig('temp/plot.png')
    # buf.seek(0)
    # plt.close()

    # return buf


    plt.figure(figsize=(10, 5))
    plt.plot(times, closes, marker='o', linestyle='-', color='b')
    plt.title(f'{pair} Prices Over Last 15 Minutes')
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.grid(True)
    plt.tight_layout()

    #buf = io.BytesIO()
    plt.savefig('temp/plot.png')
    #buf.seek(0)
    plt.close()

    #return buf