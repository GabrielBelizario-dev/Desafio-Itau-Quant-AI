import yfinance as yf
import pandas as pd
import numpy as np
from arch import arch_model
import pywt
import warnings

# Ignora avisos, úteis durante o desenvolvimento
warnings.filterwarnings('ignore')

# --- 1. CONFIGURAÇÃO E DOWNLOAD DE DADOS ---
ticker = 'PETR4.SA'
start_date = '2018-01-01'
end_date = '2024-06-30'

# Baixar dados
try:
    dados = yf.download(ticker, start=start_date, end=end_date)
    if dados.empty:
        raise ValueError("Dados não encontrados. Verifique o ticker e o período.")
except Exception as e:
    print(f"Erro ao baixar os dados: {e}")
    exit()

# Calcular retornos logarítmicos
retornos = np.log(dados['Close'] / dados['Close'].shift(1)).dropna()

# --- 2. CONFIGURAÇÃO DO BACKTEST ---
# Tamanho da janela de treino (ex: 252 dias úteis = ~1 ano)
window_size = 252
# Tamanho da janela de previsão (ex: 1 dia)
forecast_horizon = 1

# DataFrames para armazenar resultados
results_df = pd.DataFrame(index=retornos.index)
results_df['Real_Return'] = retornos
results_df['Forecasted_Volatility'] = np.nan

# --- 3. LOOP PRINCIPAL DO BACKTEST (JANELA ROLANTE) ---
print("Iniciando backtest com janela rolante...")

for i in range(window_size, len(retornos) - forecast_horizon):
    # a. Selecionar a janela de treino
    train_data = retornos.iloc[i - window_size : i]

    # b. Decomposição Wavelet
    # A wavelet 'db2' é uma escolha comum e foi usada no TCC
    # O nível de decomposição pode ser ajustado
    try:
        coeffs = pywt.wavedec(train_data, 'db2', level=2)
        # Extrair os componentes de aproximação (A) e detalhe (D)
        cA2, cD2, cD1 = coeffs
    except ValueError as e:
        # Pula se houver um erro de decomposição
        print(f"Erro na decomposição wavelet na iteração {i}: {e}. Pulando...")
        continue

    # c. Modelagem e Previsão (Simplificada)
    # A modelagem de cada componente pode ser mais complexa
    try:
        # GARCH para volatilidade (componente de detalhe)
        vol_model = arch_model(cD1, vol='Garch', p=1, q=1)
        vol_res = vol_model.fit(disp='off')
        # Previsão da volatilidade do detalhe
        vol_forecast = vol_res.forecast(horizon=forecast_horizon)
        vol_forecast_val = np.sqrt(vol_forecast.variance.iloc[-1].values[0])

        # Para o componente de aproximação (baixa frequência), usaremos a média
        # Como um placeholder. A substituição pelo ARIMA exige mais código e ajuste de parâmetros
        # Para um modelo inicial, essa simplificação é aceitável
        approx_forecast = cA2.mean()
        
        # Recompor a previsão. A soma é a maneira mais simples
        final_forecast = approx_forecast + vol_forecast_val
    
        # d. Armazenar a previsão
        results_df.loc[retornos.index[i], 'Forecasted_Volatility'] = final_forecast
        
    except Exception as e:
        print(f"Erro na modelagem GARCH na iteração {i}: {e}. Pulando...")
        continue

print("Backtest concluído.")

# --- 4. ANÁLISE E VISUALIZAÇÃO DOS RESULTADOS (SIMPLIFICADA) ---
results_df.dropna(inplace=True)

# Lógica de trading simples:
# Se a volatilidade prevista for baixa, talvez você queira tomar mais risco.
# Para este exemplo, usaremos o sinal para calcular um retorno ponderado.
results_df['Normalized_Forecast'] = results_df['Forecasted_Volatility'] / results_df['Forecasted_Volatility'].max()
results_df['Strategy_Return'] = results_df['Real_Return'] / (results_df['Normalized_Forecast'])

# Plotar os resultados (opcional, requer Plotly)
try:
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=results_df.index, y=results_df['Real_Return'].cumsum(),
                             mode='lines', name='Retorno Real Acumulado'))
    fig.add_trace(go.Scatter(x=results_df.index, y=results_df['Strategy_Return'].cumsum(),
                             mode='lines', name='Retorno da Estratégia Acumulado'))
    fig.update_layout(title=f'Backtest da Estratégia Híbrida: {ticker}',
                      xaxis_title='Data', yaxis_title='Retorno Acumulado')
    fig.show()
except ImportError:
    print("Plotly não está instalado. Não foi possível gerar o gráfico.")