import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Baixar dados (exemplo PETR4)
ticker = "PETR4.SA"
dados = yf.download(ticker, start="2020-01-01", end="2025-08-01")

# Usar apenas OHLC + Volume
dados = dados[["Open", "High", "Low", "Close", "Volume"]]

# Médias móveis
dados["MM20"] = dados["Close"].rolling(window=20).mean()
dados["MM50"] = dados["Close"].rolling(window=50).mean()
dados.dropna(inplace=True)

if dados.empty:
    print("Erro: Todos os dados foram removidos após a operação dropna. Ajuste o período de download.")
    exit()
# Criar figura com subplots (preço em cima, volume embaixo)
from plotly.subplots import make_subplots

fig = make_subplots(

    rows=1, cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],  # 70% para candles, 30% para volume
    vertical_spacing=0.05,
    subplot_titles=(f"{ticker} - Preço", "Volume")
)

# Candlestick
fig.add_trace(go.Candlestick(
    x=dados.index,
    open=dados["Open"],
    high=dados["High"],
    low=dados["Low"],
    close=dados["Close"],
    increasing_line_color="green",
    decreasing_line_color="red",
    name="Candlestick"
), row=1, col=1)

# Médias móveis
fig.add_trace(go.Scatter(
    x=dados.index, y=dados["MM20"],
    line=dict(color="blue", width=1.5),
    name="MM20"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=dados.index, y=dados["MM50"],
    line=dict(color="red", width=1.5),
    name="MM50"
), row=1, col=1)

# Volume
fig.add_trace(go.Bar(
    x=dados.index,
    y=dados["Volume"],
    name="Volume",
    marker_color="orange",
    opacity=0.5
), row=2, col=1)

# Layout
fig.update_layout(
    title=f"Gráfico de {ticker} (OHLC + MM20/MM50 + Volume)",
    xaxis_rangeslider_visible=False,
    template="plotly_dark",
    width=1000,
    height=700
)

fig.show()

