import matplotlib.pyplot as plt
import io
from datetime import datetime
import numpy as np

import plotly.subplots as ms
import plotly.graph_objects as go
import pandas as pd


def generate_plot(data: dict, pair: str) -> io.BytesIO:
    """
    Generates plot based on trading data
    """
    times = [
        datetime.fromtimestamp(int(candle[0]) / 1000)
        for candle in data["result"]["list"]
    ]
    closes = [float(candle[4]) for candle in data["result"]["list"]]

    x = np.linspace(0, 100, 100)
    y = [2 * k for k in x]

    # plt.plot(x, y)
    # buf = io.BytesIO()
    # plt.savefig('temp/plot.png')
    # buf.seek(0)
    # plt.close()

    # return buf

    plt.figure(figsize=(10, 5))
    plt.plot(times, closes, marker="o", linestyle="-", color="b")
    plt.title(f"{pair} Prices Over Last 15 Minutes")
    plt.xlabel("Time")
    plt.ylabel("Close Price")
    plt.grid(True)
    plt.tight_layout()

    # buf = io.BytesIO()
    plt.savefig("temp/plot.png")
    # buf.seek(0)
    plt.close()

    # return buf


def generate_candlesticks_volume_chart(data: dict, pair: str) -> None:
    """
    Generates candlesticks trading chart with trading volumes
    with Plotly
    """

    index = [float(candle[0]) for candle in data["result"]["list"]]
    closes = [float(candle[4]) for candle in data["result"]["list"]]
    opens = [float(candle[1]) for candle in data["result"]["list"]]
    highs = [float(candle[2]) for candle in data["result"]["list"]]
    lows = [float(candle[3]) for candle in data["result"]["list"]]
    volumes = [float(candle[5]) for candle in data["result"]["list"]]

    fig = ms.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)
    fig.add_trace(
        go.Candlestick(
            x=index,
            low=lows,
            high=highs,
            close=closes,
            open=opens,
            increasing_line_color="green",
            decreasing_line_color="red",
            row=1,
            col=1,
        )
    )

    # Add Volume Chart to Row 2 of subplot
    fig.add_trace(go.Bar(x=index, y=volumes), row=2, col=1)

    # Update Price Figure layout
    fig.update_layout(
        title=f"{pair} chart",
        yaxis1_title="price",
        yaxis2_title="volume",
        xaxis2_title="time",
        xaxis1_rangeslider_visible=False,
        xaxis2_rangeslider_visible=True,
    )
